import cubekit

print("cubekit loaded from:")
print(cubekit.__file__)

# Import from package
from cubekit.core import *
from cubekit.solver3x3 import *

print("Imports successful.")