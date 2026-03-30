from .first_layer import FirstCross, FirstCorners, FirstLayer
from .second_layer import SecondLayer
from .last_layer import LastLayer

class Solver3x3(FirstLayer, SecondLayer, LastLayer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def solve_cube(self):
        return self.solve_first_layer() + self.solve_second_layer() + self.solve_last_layer()
    
    def solve_till_second_layer(self):
        return self.solve_first_layer() + self.solve_second_layer()
    
