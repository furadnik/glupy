"""Check whether or not a graph can be colored using k colors."""
from sys import argv

from glupy.cnf import CNF
from glupy.file_parsers import graph, read_graph
from glupy.solver import Solver


def _get_variable(vertex: int, color: int, num_cols: int) -> int:
    """Get variable number."""
    return (vertex - 1) * num_cols + color


def _graph_and_colors_to_cnf(graph: graph, num_colors: int) -> CNF:
    """Generate CNF to check `num_colors`-coloring.

    Vertices indices should be positive integers. The resulting variables in the CNF have the following format:
    the `i`-th variable represents, whether or not `i//num_of_verticies`-th vertex should have `i%num_colors`-th color.
    """
    cnf = CNF()

    # each vertex only has one color.
    for vertex in graph[0]:
        # every edge has at least one color
        cnf.add_clause([_get_variable(vertex, x, num_colors) for x in range(1, num_colors + 1)])

        # no edge has two colors
        for color in range(1, num_colors):
            for other_color in range(color + 1, num_colors + 1):
                cnf.add_clause(
                    [-_get_variable(vertex, color, num_colors), -_get_variable(vertex, other_color, num_colors)]
                )

    # each edge has different colors on its ends.
    for vertex, other_vertex in graph[1]:
        for color in range(1, num_colors + 1):
            cnf.add_clause([-_get_variable(vertex, color, num_colors), -_get_variable(other_vertex, color, num_colors)])

    return cnf


def check_graph_coloring(graph: graph, chromatic_number: int, timeout: float | None = None) -> bool | None:
    """Check coloring, or return None if timeout is reached."""
    graph_cnf = _graph_and_colors_to_cnf(graph, chromatic_number)
    solver = Solver()
    return solver.solve(graph_cnf, timeout)


def main(graph_file: str, chromatic_number: int, timeout: int | None = None) -> bool | None:
    """Check coloring, or return None if timeout is reached."""
    with open(graph_file, "r") as f:
        graph = read_graph(f)

    return check_graph_coloring(graph, chromatic_number, timeout)


if __name__ == '__main__':
    if len(argv) < 3:
        raise ValueError("Invalid parameters")
    print(main(argv[1], int(argv[2])))
