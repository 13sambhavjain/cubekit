# cubekit

A modular Python toolkit for cube simulation and human-style solving workflows.

`cubekit` provides structured cube modeling utilities and solver pipelines designed to mimic human solving strategies such as CFOP. The project focuses on modular design, extensibility, and large-scale validation of solving logic.

Install from PyPI:

pip install cubekit

---

## Features

- Modular cube simulation engine
- Human-style solving workflows (CFOP-based 3x3 solver)
- Extensible solver architecture
- Flexible cube representation
- Random scramble generation
- Large-scale validation utilities
- Designed for future visualization and teaching tools

---

## Installation

Install from PyPI:

pip install cubekit

Requires:

- Python 3.10+

---

## Quick Example

```python
from cubekit.core import Cube3x3
from cubekit.solver3x3 import Solver3x3

# Create cube
cube = Cube3x3()

# Apply scramble
cube.applyScramble("R U R' U'")

# Solve cube
solver = Solver3x3(cube)

solution = solver.solve()

print("Solution:")
print(solution)
```

---

## Project Structure

    cubekit/
    │
    ├── core/
    │   Cube representation
    │   Move definitions
    │   Rotation logic
    │
    ├── solver3x3/
    │   CFOP-based solving logic
    │   OLL / PLL algorithms
    │   Step-based solving workflow
    │
    └── examples/
        Validation utilities
        Stress-testing scripts

---

## Solver Design

The current implementation includes a human-style CFOP-based 3x3 solver.

Stages include:

- Cross formation  
- F2L pair solving  
- OLL (Orientation of Last Layer)  
- PLL (Permutation of Last Layer)  

The solver dynamically identifies cube state and applies appropriate solving sequences depending on piece configuration.

Each solving step generates move sequences along with descriptive comments explaining the purpose of that step, enabling human-readable solving workflows.

---

## Validation

The solver has been tested using large randomized scramble sets.

Validation includes:

- Random scramble generation  
- Multi-case solving workflows  
- Repeated large-scale test execution  
- State verification after solving  

Stress testing has been performed across millions of cube states with scramble depths up to 20 moves (God's Number range).

---

## Design Philosophy

`cubekit` is designed around:

- Human-readable solving workflows  
- Modular architecture  
- Extensible solver pipelines  
- Separation between cube modeling and solving logic  
- Reusable components across different solver types  

The cube engine supports flexible configuration of colors, face identifiers, and cube sizes, allowing future expansion beyond 3x3 solving.

---

## Planned Features

- Visualization tools  
- Django-based teaching interface  
- Support for additional solving methods  
- Support for multiple cube sizes  
- Plugin-based solver extensions  
- Logging-based validation reporting  
- Human-readable solving visualizations  

---

## Use Cases

`cubekit` is designed for:

- Educational tools  
- Algorithm experimentation  
- Human-style cube solving simulation  
- Solver validation workflows  
- Visualization projects  
- Teaching cube-solving logic  

---

## Version

Current version:

v0.0.1 — Initial public release

---

## License

MIT License

Copyright (c) 2025 Sambhav Jain