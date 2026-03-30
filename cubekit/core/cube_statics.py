# standard library imports
from functools import cache
from collections.abc import Callable
import random
# core imports
from .colors import Color, Colors
from .directions import SideDirections, Direction
from .moves import Moves, Move
from .face import Face, FaceId
from .shortnames import *
from .formula_notations import *

class CubeStatics():
    # colors = [w,r,g,y,o,b]
    # sturcture =   # w
                    # b o
                    # y g
                        # r
    def __getitem__(self, index: FaceId) -> Face: ... #type: ignore
    faceIds = Colors()
    colors = Colors() # [w, b, r, g, y, o] -  with some cyclic Functionalities
    side_directions = SideDirections() # [up, right, down, left] - with some cyclic Functionalities
    direction2faceId: dict[FaceId, dict[Direction, FaceId]] = { # mapping SideDirection to Face center color
        w: {right:o, down:b, left:r, up:g, back:y},
        y: {right:g, down:r, left:b, up:o, back:w},
        r: {right:w, down:b, left:y, up:g, back:o},
        o: {right:g, down:y, left:b, up:w, back:r},
        b: {right:o, down:y, left:r, up:w, back:g},
        g: {right:w, down:r, left:y, up:o, back:b}
    }
    faceId2direction: dict[FaceId, dict[FaceId, Direction]] = { # mapping Face center color to SideDirection
        w: {o:right, b:down, r:left, g:up, y:back},
        y: {g:right, r:down, b:left, o:up, w:back},
        r: {w:right, b:down, y:left, g:up, o:back},
        o: {g:right, y:down, b:left, w:up, r:back},
        b: {o:right, y:down, r:left, w:up, g:back},
        g: {w:right, r:down, y:left, o:up, b:back}
    }
    movementDirection2index: dict[Direction, tuple[str, int]] = { # mapping movement of SideDirection to row/column index
        up: ('x', 0),
        down: ('x', -1),
        right: ('y', -1),
        left: ('y', 0)
    }

    @staticmethod
    def faceId2color(faceid: FaceId) -> Color:
        return faceid
    
    @staticmethod
    def color2faceId(color: Color) -> FaceId:
        return color

    @staticmethod
    def turns4directionchange(start_direction: Direction, end_direction: Direction, check: bool=True) -> int:
        start_index = CubeStatics.side_directions.index(start_direction)
        end_index = CubeStatics.side_directions.index(end_direction)
        if check and (start_index < 0 or end_index < 0):
            raise ValueError(f"Given Directions are not in side_direction, ({start_direction=}, {end_direction=})")
        return (end_index - start_index)%4
    
    @staticmethod
    def turns4faceIdchange(turning_faceId: FaceId, start_faceId: FaceId, end_faceId: FaceId) -> int:
        start_direction = CubeStatics.faceId2direction[turning_faceId][start_faceId]
        end_direction = CubeStatics.faceId2direction[turning_faceId][end_faceId]
        return CubeStatics.turns4directionchange(start_direction, end_direction)
    
    @staticmethod
    def move4faceIdchange(turning_faceId: FaceId, start_faceId: FaceId, end_faceId: FaceId) -> Move:
        return Move(turning_faceId, CubeStatics.turns4faceIdchange(turning_faceId, start_faceId, end_faceId))

    @staticmethod
    def relative_direction2faceid(front: FaceId, top: FaceId, direction: Direction) -> FaceId:
        rotate = CubeStatics.side_directions.index(CubeStatics.faceId2direction[front][top])
        if direction == right:
            ans = CubeStatics.direction2faceId[front][CubeStatics.side_directions[(rotate+1)%4]]
        elif direction == left:
            ans = CubeStatics.direction2faceId[front][CubeStatics.side_directions[(rotate-1)%4]]
        elif direction == up:
            ans = top
        elif direction == down:
            ans = CubeStatics.direction2faceId[top][back]
        elif direction == back:
            ans = CubeStatics.direction2faceId[front][back]
        else:
            ans = front        
        return ans
    
    @cache
    @staticmethod
    def direction_map(front: FaceId, top: FaceId) -> dict[str, FaceId]:
        try:
            rotate = CubeStatics.side_directions.index(CubeStatics.faceId2direction[front][top])
        except Exception as e:
            raise ValueError(f"Invalid front/top pair: {front=}, {top=}") from e
        direction_map: dict[str, FaceId] = {
            'U': top,
            'R': CubeStatics.direction2faceId[front][CubeStatics.side_directions[(rotate+1)%4]],
            'D': CubeStatics.direction2faceId[top][back],
            'L': CubeStatics.direction2faceId[front][CubeStatics.side_directions[(rotate+3)%4]],
            'B': CubeStatics.direction2faceId[front][back],
            'F': front
        }
        return direction_map

        
    @staticmethod
    def formula2Moves(front: FaceId, top: FaceId, formula: str) -> Moves:
        formula = formula.replace(" ", "")
        moves = Moves()
        direction_map = CubeStatics.direction_map(front, top)
        i = 0
        n = len(formula) - 1
        def cube_rotation2fronttop(rotation: str, turns: int = 1) -> tuple[FaceId, FaceId]:
            turns %= 4
            nonlocal direction_map
            front = direction_map['F']
            top = direction_map['U']
            cube_rotation_map = {
                ('x', 1): (direction_map['D'], front),
                ('x', 2): (direction_map['B'], direction_map['D']),
                ('x', 3): (top, direction_map['B']),
                ('y', 1): (direction_map['R'], top),
                ('y', 2): (direction_map['B'], top),
                ('y', 3): (direction_map['L'], top),
                ('z', 1): (front, direction_map['L']),
                ('z', 2): (front, direction_map['D']),
                ('z', 3): (front, direction_map['R']),
            }
            return cube_rotation_map[(rotation, turns)]
        
        def wide_move2fronttop(wide_move: str, turns: int) -> tuple[FaceId, FaceId]:
            if wide_move == 'f':
                return cube_rotation2fronttop('z', turns)
            elif wide_move == 'r':
                return cube_rotation2fronttop('x', turns)
            elif wide_move == 'u':
                return cube_rotation2fronttop('y', turns)
            elif wide_move == 'l':
                return cube_rotation2fronttop('x', -turns)
            elif wide_move == 'b':
                return cube_rotation2fronttop('z', -turns)
            elif wide_move == 'd':
                return cube_rotation2fronttop('y', -turns)
            raise NotImplementedError
        
        def changesby_slice_move(slice: str, turns: int) -> None:
            nonlocal moves, direction_map
            if slice == 'M':
                moves.append(Move(direction_map['L'], turns))
                moves.append(Move(direction_map['R'], -turns))
                direction_map = CubeStatics.direction_map(*cube_rotation2fronttop('x', -turns))
            elif slice == 'E':
                moves.append(Move(direction_map['D'], turns))
                moves.append(Move(direction_map['U'], -turns))
                direction_map = CubeStatics.direction_map(*cube_rotation2fronttop('y', -turns))
            elif slice == 'S':
                moves.append(Move(direction_map['F'], turns))
                moves.append(Move(direction_map['B'], -turns))
                direction_map = CubeStatics.direction_map(*cube_rotation2fronttop('z', turns))
            else:
                raise NotImplementedError

        def char_turns2changes(char: str, turns: int) -> None:
            nonlocal moves, direction_map
            if char in BASIC_MOVES:
                moves.append(Move(direction_map[char], turns))
            elif char in WIDE_MOVES:
                # opp move and cube_rotation
                moves.append(Move(CubeStatics.direction2faceId[direction_map[char.upper()]][back], turns))
                direction_map = CubeStatics.direction_map(*wide_move2fronttop(char, turns))
            elif char in ROTATION_MOVES:
                # cube rotation
                direction_map = CubeStatics.direction_map(*cube_rotation2fronttop(char, turns))
            elif char in SLICE_MOVES:
                changesby_slice_move(char, turns)
            else: 
                raise NotImplementedError(f"{char} as a formula move is not implemented.")
            

        while i < n:
            char = formula[i]
            turns = 3 if formula[i+1] in ANTICLOCKWISE_TURN else (2 if formula[i+1] in DOUBLE_TURN else 1)
            i += 1 if turns == 1 else 2
            char_turns2changes(char, turns)
        if i == n:
            char_turns2changes(formula[i], 1)
        return moves
    
    
    
    @classmethod
    @cache
    def get_neighbors(cls, face_id: FaceId) -> list[tuple[FaceId, Direction]]:
        """Return 4 neighboring faces of `face_id` in order: right, up, left, down."""
        return [
            (cls.direction2faceId[face_id][right],  cls.faceId2direction[cls.direction2faceId[face_id][right]][face_id]),
            (cls.direction2faceId[face_id][up],     cls.faceId2direction[cls.direction2faceId[face_id][up]][face_id]),
            (cls.direction2faceId[face_id][left],   cls.faceId2direction[cls.direction2faceId[face_id][left]][face_id]),
            (cls.direction2faceId[face_id][down],   cls.faceId2direction[cls.direction2faceId[face_id][down]][face_id]),
        ]

    @staticmethod
    def getSolvedState(size:int = 3, faceId2fillColor: Callable[[FaceId], Color] = lambda x: x)  -> dict[FaceId, Face]:
        """Return the solved state of a Cube of given size."""
        return {
            faceId: Face(size, faceId2fillColor(faceId))
            for faceId in CubeStatics.faceIds
        }
    
    @staticmethod
    def get_randomScramble(limit: int = 20, efficient=False) -> Moves:
        moves: Moves = Moves(efficient=True)
        for _ in range(limit):
            moves.append(Move(faceId=random.choice(CubeStatics.faceIds), turns=random.choice([1,2,3])))
        while len(moves) < limit:
            moves.append(Move(faceId=random.choice(CubeStatics.faceIds), turns=random.choice([1,2,3])))
        return moves