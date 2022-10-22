from pathlib import Path

from glupy.cnf import CNF
from glupy.solver import Solver

cnf = CNF.from_file(Path("/home/tmq/tmp/ukol1/priklad_bipartitnost/2.graph.cnf"))
solver = Solver("/home/tmq/tmp/ukol1/glucose_static")

print(solver.solve_model(cnf))
