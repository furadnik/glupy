"""The Glucose Wrapper itself."""
import subprocess
import tempfile
from pathlib import Path

from .cnf import CNF


class Solver:
    """A solver object for SAT."""

    def __init__(self, glucose_path: str = "./glucose_static") -> None:
        """Initialize the solver."""
        self._glucose = glucose_path
        self._tempdirs: list[tempfile.TemporaryDirectory] = []

    def _run_subprocess(self, args: list[str], wait_time: int | None) -> str:
        """Run the glucose process. Wait for answer."""
        process = subprocess.Popen([self._glucose] + args, stdout=subprocess.PIPE, universal_newlines=True)
        return process.communicate(timeout=wait_time)[0].strip().split("\n")[-1]

    def _tempfile(self, cnf: CNF) -> str:
        """Generate a tempfile with CNF."""
        dir = tempfile.TemporaryDirectory()
        self._tempdirs.append(dir)
        file = Path(dir.name) / "in"
        cnf.to_file(file)
        return str(file)

    def solve(self, cnf: CNF, timeout: int | None = None) -> bool:
        """Solve CNF, return whether satisfiable."""
        return self._run_subprocess([self._tempfile(cnf)], timeout) == "s SATISFIABLE"

    def __del__(self) -> None:
        """Cleanup tempfiles."""
        for dir in self._tempdirs:
            dir.cleanup()

    def solve_model(self, cnf: CNF, timeout: int | None = None) -> list[int] | None:
        """Get model, or return None if no exists."""
        res = self._run_subprocess(["-model", self._tempfile(cnf)], timeout)
        if not res or res.startswith("s "):
            return None

        return [int(x) for x in res[2:].split(" ")]
