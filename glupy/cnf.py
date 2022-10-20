"""Represent a CNF statement."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, TextIO


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


class CNF:
    """A representation of a CNF statement."""

    def __init__(self, *clauses: list[int]) -> None:
        """Save initial clauses."""
        self._clauses: list[list[int]] = list(clauses) or []

        self._variables = 0
        for clause in self._clauses:
            self._add_variables(clause)

    def _add_variables(self, clause: list[int]) -> None:
        """Recalculate the number of variables."""
        for var in clause:
            self._variables = max(self._variables, abs(var))

    @property
    def variables(self) -> int:
        """Return the number of variables used."""
        return self._variables

    def add_clause(self, clause: list[int]) -> None:
        """Add a clause."""
        if len(clause) >= 1 and 0 not in clause:
            self._clauses.append(clause)
            self._add_variables(clause)
        else:
            raise ValueError("Invalid clause.")

    def to_file(self, path: Path) -> None:
        """Write the CNF clauses to a file."""
        # concatenate clauses into a string
        cnf_str = '\n'.join([' '.join(map(str, clause)) + ' 0' for clause in self._clauses])

        with open(path, 'w') as f:
            f.write(f'p cnf {self.variables} {len(self._clauses)}\n')
            f.write(cnf_str)

    def add_from_file(self, path: Path) -> None:
        """Add clauses from a cnf file."""
        with open(path, "r") as f:
            for clause in cnf_parser(f):
                self.add_clause(clause)

    @classmethod
    def from_file(self, path: Path) -> CNF:
        """Get a CNF from a file."""
        cnf = CNF()
        cnf.add_from_file(path)
        return cnf
