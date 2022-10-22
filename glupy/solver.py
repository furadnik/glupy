"""The Glucose Wrapper itself."""
import subprocess, os, signal, time
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
        start_time = time.time()
        while wait_time is None or time.time() < start_time + wait_time:
            return_code = process.poll()
            if return_code is not None:
                return process.stdout.readlines()[-1].strip()

        process.kill()
        return ""

    def _tempfile(self, cnf: CNF) -> str:
        """Generate a tempfile with CNF."""
        dir = tempfile.TemporaryDirectory()
        self._tempdirs.append(dir)
        file = Path(dir.name) / "in"
        cnf.to_file(file)
        return str(file)

    def solve(self, cnf: CNF, timeout: float | None = None) -> bool | None:
        """Solve CNF, return whether satisfiable."""
        r = self._run_subprocess([self._tempfile(cnf)], timeout)
        if r:
            return r == "s SATISFIABLE"
        return None

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
