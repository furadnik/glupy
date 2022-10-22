"""Approximate the chromatic number."""
import itertools
import random
from sys import argv
from typing import Iterable

from glupy.file_parsers import graph, read_graph

from .check_graph_coloring import check_graph_coloring


def roundrobin(*iterables):
    """Roundrobin('ABC', 'D', 'EF') --> A D E B F C."""
    pending = len(iterables)
    nexts = itertools.cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = itertools.cycle(itertools.islice(nexts, pending))


def index_gen(lower: int, upper: int) -> Iterable[int]:
    if lower == upper:
        yield lower
        return

    avg = int((lower + upper) // 2)
    yield avg

    gen1 = index_gen(lower, avg)
    gen2 = index_gen(avg + 1, upper)

    for x, y in itertools.zip_longest(gen1, gen2):
        yield x
        yield y


def approx_graph_chromatic_number(graph: graph) -> int:
    """TODO: implement later."""
    upper = len(graph[0])
    lower = 0
    timeout = 3.0
    multiplier = 2

    while lower + 1 < upper:
        for i in range(lower + 1, upper):
            r = check_graph_coloring(graph, i, timeout)
            if r:
                upper = i
                break
            elif r is False:
                lower = i

        print(f"{int(timeout)}: {lower} < C <= {upper}")
        timeout *= multiplier

    return upper


def main(graph_file: str) -> int:
    """Check coloring, or return None if timeout is reached."""
    with open(graph_file, "r") as f:
        graph = read_graph(f)

    return approx_graph_chromatic_number(graph)


if __name__ == '__main__':
    if len(argv) < 2:
        raise ValueError("Invalid parameters")
    print(main(argv[1]))
