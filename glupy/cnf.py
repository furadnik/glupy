"""Represent a CNF statement."""
from __future__ import annotations

from pathlib import Path

from .file_parsers import cnf_parser


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
