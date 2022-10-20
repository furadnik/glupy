import tempfile
from pathlib import Path
from unittest import TestCase

from glupy.cnf import CNF


class TestCNF(TestCase):

    def setUp(self) -> None:
        self.cnf = CNF()
        self._tmpdir = tempfile.TemporaryDirectory()
        self.file = Path(self._tmpdir.name) / "foobar"

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_init_empty(self):
        self.assertListEqual(self.cnf._clauses, [])
        self.assertEqual(self.cnf.variables, 0)

    def test_init_nonempty(self):
        cnf = CNF([1])
        self.assertEqual(cnf._clauses, [[1]])
        self.assertEqual(cnf.variables, 1)

    def test_add_clause_valid(self):
        self.cnf.add_clause([-1, 2])
        self.assertEqual(self.cnf._clauses, [[-1, 2]])
        self.assertEqual(self.cnf.variables, 2)

    def test_add_clause_invalid(self):
        self.assertRaises(ValueError, self.cnf.add_clause, [-1, 0, 2])

    def test_to_file(self):
        self.cnf.add_clause([-1, 2])
        self.cnf.add_clause([1, 3])
        self.cnf.to_file(self.file)
        self.assertEqual(self.file.read_text(), """
p cnf 3 2
-1 2 0
1 3 0
                         """.strip())

    def test_from_file_valid(self):
        self.file.write_text("""
p cnf 20 40
1 2 3 0
-1 2 -3 0
                             """.strip())
        self.assertEqual(
            CNF.from_file(self.file)._clauses,
            [
                [1, 2, 3],
                [-1, 2, -3]
            ])

    def test_from_file_invalid_header(self):
        self.file.write_text("""
asdfasdf lasmdfkasdmflp
1 2 3 0
-1 2 -3 0
                             """.strip())
        self.assertRaises(
            ValueError, CNF.from_file, self.file)

    def test_from_file_wrong_header(self):
        self.file.write_text("""
p asdf 34 45
1 2 3 0
-1 2 -3 0
                             """.strip())
        self.assertRaises(
            ValueError, CNF.from_file, self.file)

    def test_from_file_good_header_but_wtf(self):
        self.file.write_text("""
p cnf 34 45
-1 2 -asdf3
asdfasd1 2sdf 3 0
                             """.strip())
        self.assertRaises(
            ValueError,
            CNF.from_file, self.file)
