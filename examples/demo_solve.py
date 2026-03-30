from cubekit.core import Cube
from cubekit.solver3x3 import Solver3x3

cube = Cube()

cube.apply_scramble("R U R' U'")

solver = Solver3x3(cube)

solution = solver.solve_cube()

print("Solution:")
print(solution)