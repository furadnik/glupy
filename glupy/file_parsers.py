"""Module containing file parsers."""
from typing import Iterable, TextIO

vert_list = list[int]
edge_list = list[tuple[int, int]]
graph = tuple[vert_list, edge_list]


def cnf_parser(file: TextIO) -> Iterable[list[int]]:
    """Parse a CNF file."""
    header = file.readline()

    if not header.startswith("p cnf "):  # not checking the header numbers
        raise ValueError("Wrong CNF file format.")

    for line in file.readlines():
        if not (line.endswith(" 0") or line.endswith(" 0\n")):
            raise ValueError("Incorrect CNF line ")

        # leave default int conversion error
        yield [int(x) for x in line[:-2].strip().split(" ")]


def read_graph(file: TextIO) -> graph:
    """Parse a graph file."""
    vertices, edges = [], []
    vert_num = -1
    edg_num = -1
    for line in file.readlines():
        if line.startswith('c '):  # ignore comments
            continue
        if line.startswith('e '):  # add an edge, check vertex number are consistent
            parts = line.split(' ')
            u, v = int(parts[1]), int(parts[2])
            if u > vert_num or v > vert_num:
                print('Warning: invalid vertex number found in edge:', line)
            edges.append((u, v))

        if line.startswith('p edge'):  # parse problem specification
            parts = line.split(' ')
            vert_num = int(parts[2])
            edg_num = int(parts[3])
            vertices = list(range(1, vert_num + 1))

    if edg_num != len(edges):
        print('Warning: number of edges does not match file header: %d != %d' % (len(edges), edg_num))

    return vertices, edges
