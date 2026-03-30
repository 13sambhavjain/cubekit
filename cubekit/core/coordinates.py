# core imports
from .face import FaceId, Position

class Coords():
    # """Coordinates of a Color in a Cube with fix center"""
    def __init__(self, face_id: FaceId, x: int=None, y: int=None, *, pos:Position=None): #type: ignore
        self.face_id: FaceId = face_id
        self.pos = pos
        if x != None and y != None:
            self.pos: Position = Position(x, y) #type: ignore
        elif pos is None:
            raise ValueError(f"Need to pass either pos or x and y both")

    @property
    def x(self) -> int:
        return self.pos.x
    @x.setter
    def x(self, value: int):
        self.pos.x = value

    @property
    def y(self) -> int:
        return self.pos.y
    @y.setter
    def y(self, value: int):
        self.pos.y = value

    def __iter__(self):
        yield self.face_id
        yield self.x
        yield self.y

    def __getitem__(self, index: int) -> FaceId|int:
        index %= 3
        if index == 0:
            return self.face_id
        elif index == 1:
            return self.x
        else: # index == 2
            return self.y

    def __setitem__(self, index: int, value: FaceId|int) -> None:
        index %= 3
        if index == 0:
            self.face_id = value # type: ignore
        elif index == 1:
            self.x = value # type: ignore
        else: # index == 2
            self.y = value # type: ignore

    def __str__(self) -> str:
        return f'({self.face_id}, {self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in vars(self).items())})'
    
    def __eq__(self, other: object):
        if isinstance(other, Coords):
            return self.face_id == other.face_id and self.x == other.x and self.y == other.y
        elif isinstance(other, tuple) and len(other) == 3:
            return self.face_id == other[0] and self.x == other[1] and self.y == other[2]
        return NotImplemented
        
    def __hash__(self):
        return hash((self.face_id, self.x, self.y))
    
