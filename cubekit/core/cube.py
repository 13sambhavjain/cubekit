# standard lib imports
from copy import copy, deepcopy
# core imports
from .colors import Colors, Color
from .face import Face, FaceId, FaceIds
from .coordinates import Position, Coords
from .directions import SideDirections, Direction
from .shortnames import *
from .cube_movements import CubeMovements
from .cube_statics import CubeStatics

class Cube(CubeMovements, CubeStatics):
    """Class(Structur and functions) of a 3x3 Rubick's Cube"""

    def __init__(self, *, 
                 size:int = 3, 
                 start_faceId: FaceId = w, 
                 default_print_format: str = 'i', 
                 state: dict[FaceId, Face]=None #type: ignore
                 ) -> None:
        """Initialize a Cube(Solved) of given size."""
        self.size: int = size
        self.state: dict[FaceId, Face] = state if state else Cube.getSolvedState(self.size)
        self.start_faceId: FaceId = start_faceId
        self.default_print_format: str = default_print_format

    def isSolved(self) -> bool:
        """Check if the Cube is in solved state."""
        return self.state == Cube.getSolvedState(self.size)
    
    def __getitem__(self, face_id: FaceId) -> Face:
        return self.state[face_id]

    def __setitem__(self, face_id: FaceId, value: Face) -> None:
        self.state[face_id] = value

    def __contains__(self, face_id: FaceId) -> bool:
        return face_id in self.state

    def __format__(self, format_spec: str) -> str:
        """
        Prints the cube layout starting from self.start_faceId in a diagonal layout:
            w
            b  o
               y  g
                  r
        Traverses down and right directions dynamically until right loops back to start.
        """
        def fmt(face_id):
            return format(self[face_id], format_spec).split('\n')
        def visible_len(s: str) -> int:
            """Return visible length of string ignoring ANSI color codes."""
            n = 0
            i = 0
            while i < len(s):
                if s[i] == "\x1b":  # start of ANSI escape sequence
                    # skip until 'm' or end of string
                    i += 1
                    while i < len(s) and s[i] != "m":
                        i += 1
                    i += 1  # skip the 'm' itself
                else:
                    n += 1
                    i += 1
            return n

        cameDown = False if Cube.faceIds.index(self.start_faceId)%2 else True
        gap = "  "  # space between adjacent faces in a row
        rightCount = 0
        start_face = self.start_faceId
        current_face = Cube.direction2faceId[start_face][down if cameDown else right]
        current_lines = fmt(start_face)
        face_width = visible_len(current_lines[0])
        ans = []
            
        while current_face != start_face:
            # collect faces in the current "row"
            if cameDown:
                ans += current_lines + [""]
                current_lines = fmt(current_face)
                indent = (" " * (face_width) + gap) * rightCount
                for i in range(len(current_lines)):
                    current_lines[i] = indent + current_lines[i]
                current_face = Cube.direction2faceId[current_face][right] #went to right
                cameDown = False
            else: # came right
                # ans += current_lines (already done in else case)
                add2lines = fmt(current_face)
                for i in range(len(current_lines)):
                    current_lines[i] += gap + add2lines[i]
                current_face = Cube.direction2faceId[current_face][down] # went down
                cameDown = True
                rightCount += 1
                
        ans += current_lines

        return "\n".join(ans)
    
    def __str__(self) -> str:
        return self.__format__(self.default_print_format)
    
    def get(self, coords: Coords) -> Color:
        "Given Coords returns the Color at coords in cube state"
        return self.state[coords.face_id].get(coords.pos)
    
    def set(self, coords: Coords, value: Color):
        "Given Coords returns the Color at coords in cube state"
        self.state[coords.face_id].set(coords.pos, value)
    
if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

    cube = Cube(start_faceId=b,default_print_format='coloredinitial')
    moves = cube.apply_formula(w, g, 'RUR`URUUR`')
    print(cube, moves)
    moves = cube.apply_formula(y, g, 'RUR`URUUR`UU')
    print(cube, moves)
    moves = cube.apply_formula(y, g, 'RUR`URUUR`')
    print(cube, moves)
    # moves = cube.apply_formula(o, g, 'RUR`URUUR`')
    # moves = cube.apply_formula(w, g, 'RUR`URUUR`')
    # moves = cube.apply_formula(y, g, 'RUR`URUUR`')
    # for move in moves:
    #     cube.make_move(move)
    #     print(move, cube, sep='\n')
    # print("*********************************************")
    # moves = cube.formula2Moves(y, g, 'RUR`URUUR`')
    # for move in moves:
    #     cube.make_move(move)
    #     print(move, cube, sep='\n')

