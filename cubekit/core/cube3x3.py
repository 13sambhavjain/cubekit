#standard lib imports
from functools import cache
# core imports
from .coordinates import Position, Coords
from .cube_statics import CubeStatics
from .cube import Cube
from .directions import Direction
from .shortnames import *
from .face import FaceIds, FaceId

class Cube3x3Statics(CubeStatics):
    sideDirection2edgePosition: dict[Direction, Position] = { # Coordinate of edges in a face grid of 3x3 Cube
        up: Position(0,1),
        right: Position(1, 2),
        down: Position(2, 1),
        left: Position(1, 0)
    }

    corner_positions: list[Position] = [
        Position(0, 0), Position(0, 2), Position(2, 2), Position(2, 0)
    ]
    edge_positions: list[Position] = [
        Position(0, 1), Position(1, 2), Position(2, 1), Position(1, 0)
    ]
    corner_coords_sets :list[set[Coords]]= [
        {Coords(w, 0, 0), Coords(g, 2, 2), Coords(r, 0, 2)},
        {Coords(w, 0, 2), Coords(o, 0, 2), Coords(g, 0, 2)},
        {Coords(w, 2, 0), Coords(b, 0, 0), Coords(r, 2, 2)},
        {Coords(w, 2, 2), Coords(b, 0, 2), Coords(o, 0, 0)},
        {Coords(y, 0, 0), Coords(b, 2, 2), Coords(o, 2, 0)},
        {Coords(y, 0, 2), Coords(o, 2, 2), Coords(g, 0, 0)},
        {Coords(y, 2, 0), Coords(b, 2, 0), Coords(r, 2, 0)},
        {Coords(y, 2, 2), Coords(g, 2, 0), Coords(r, 0, 0)}
    ]
    @staticmethod
    def BackEdgeCoords(coords: Coords) -> Coords:
        """Given edge coordinates (i, j)(front), return the opposite(back) edge coordinates."""
        # implement edge check
        i, j = coords.pos
        if (i+j) == 3:
            return Coords(Cube.direction2faceId[coords.face_id][back], i-1, j-1)
        else: #if edge then i+j == 1
            return Coords(Cube.direction2faceId[coords.face_id][back], i+1, j+1)

    @staticmethod
    def cornerAfterRotation(coords, rotatingFace: FaceId, check=True) -> Coords:
        if check:
            coords.pos in Cube3x3Statics.corner_positions
        raise NotImplementedError
        c,i,j = coords
        newFace = Cube.direction2color[rotatingFace][Cube.directions[Cube.directions.index(Cube.color2direction[rotatingFace][c]) - 3]]
        increment = (Cube.directions.index(Cube.color2direction[c][newFace]) - Cube.directions.index(Cube.color2direction[newFace][c]))%4
        if increment == 2:
            return newFace, i, j
        else:
            return newFace, *Cube.cornerCoord[(Cube.cornerCoord.index((i,j)) + increment)%4]

    @staticmethod
    def EdgeOtherSide(coords: Coords) -> Coords:
        """Given coords of one side of an edge piece, 
        return the coords of the other side of that edge piece."""      
        face_id, i, j = coords
        ind = int(CubeStatics.colors.index(face_id))
        k = (3 - (i + j))//2
        if (i + j)&1:
            # edges
            return Coords(CubeStatics.colors[(ind + 1 + k*3 + ((ind + (i&1))&1))%6], k + (ind&1), k + ((ind + 1)&1))
        else:
            raise ValueError
    
    @cache
    @staticmethod
    def corner_other_coords(corner_coords: Coords) -> set[Coords]:
        # raise NotImplementedError
        # corner
        for corner_coord_set in Cube3x3.corner_coords_sets:
            if corner_coords in corner_coord_set:
                return corner_coord_set - {corner_coords}
        else:
            raise ValueError(f'Given coords are not of a corner {corner_coords!r}')
        
    @staticmethod
    def is_corner(position: Position|Coords) -> bool:
        if isinstance(position, Coords):
            return position.pos in Cube3x3Statics.corner_positions
        return position in Cube3x3Statics.corner_positions
    
    @staticmethod
    def is_edge(position: Position|Coords) -> bool:
        if isinstance(position, Coords):
            return position.pos in Cube3x3Statics.edge_positions
        return position in Cube3x3Statics.edge_positions
    
    @staticmethod
    def corner_coords():
        for face_id in Cube3x3.faceIds:
            for pos in Cube3x3.corner_positions:
                yield Coords(face_id, *pos)

    @staticmethod
    def edge_coords():
        for face_id in Cube3x3.faceIds:
            for pos in Cube3x3.edge_positions:
                yield Coords(face_id, *pos)
    
class Cube3x3(Cube, Cube3x3Statics):
    def __init__(self, *args, **kwargs):
        Cube.__init__(self, size=3, *args, **kwargs)
    






