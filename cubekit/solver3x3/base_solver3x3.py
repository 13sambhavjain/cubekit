from ..core import Cube3x3, FaceId, Color, Coords, back
from copy import deepcopy
class BaseSolver3x3():
    def __init__(self, cube: Cube3x3, 
                 start_faceid :FaceId=None, #type: ignore
                 change_original: bool=True) ->  None: 
        if not change_original:
            cube = deepcopy(cube)
        self.cube: Cube3x3 = cube
        self.start_faceid: FaceId = start_faceid if start_faceid else self.cube.start_faceId
        self.start_color: Color = Cube3x3.faceId2color(self.start_faceid)
        self.last_faceid: FaceId = Cube3x3.direction2faceId[self.start_faceid][back]
        self.last_color: Color = Cube3x3.faceId2color(self.last_faceid)

    def __getattr__(self, name):
        return getattr(self.cube, name)
    
    def check_first_cross(self) -> bool:
        face = self.cube.state[self.start_faceid]
        for position in self.cube.edge_positions:
            if face.get(position) != self.start_color:
                return False
        return True
    
    def check_first_corners(self) -> bool:
        face = self.cube.state[self.start_faceid]
        for position in self.cube.corner_positions:
            if face.get(position) != self.start_color:
                return False
        return True
    
    def check_first_layer(self) -> bool:
        face = self.cube.state[self.start_faceid]
        for i in range(self.cube.size):
            for j in range(self.cube.size):
                if face[i][j] != self.start_color:
                    return False
        return True

    def check_second_layer(self) -> bool:
        for faceid in self.side_faceids:
            face_color = Cube3x3.faceId2color(faceid)
            not_to_check = Cube3x3.faceId2direction[faceid][self.start_faceid], Cube3x3.faceId2direction[faceid][self.last_faceid]
            for direction in Cube3x3.side_directions:
                if direction in not_to_check:
                    continue
                pos = Cube3x3.sideDirection2edgePosition[direction]
                if self.cube.state[faceid].get(pos) != face_color:
                    return False
        return True
    
    def check_solved(self) -> bool:
        for faceid in self.cube.state:
            face_color = Cube3x3.faceId2color(faceid)
            for x in range(self.cube.size):
                for y in range(self.cube.size):
                    if self.cube.state[faceid][x][y] != face_color:
                        return False
        return True

    
    def checkRaise_start_color_on_startface_coords(self, coords: Coords):
        if coords.face_id != self.start_faceid:
            raise ValueError("Coords are not on start face." + repr(coords))
        if self.cube.get(coords) != self.start_color:
            raise ValueError("At coords it is not start color." + repr(coords))
        
    def checkRaise_start_color_on_lastface_coords(self, coords: Coords):
        if coords.face_id != self.last_faceid:
            raise ValueError("Coords are not on last face." + repr(coords))
        if self.cube.get(coords) != self.start_color:
            raise ValueError("At coords it is not start color." + repr(coords))
    
    def checkRaise_start_color_on_sideface_coords(self, coords: Coords):
        if coords.face_id == self.start_faceid or coords.face_id == self.last_faceid:
            raise ValueError("Coords are not on last face." + repr(coords))
        if self.cube.get(coords) != self.start_color:
            raise ValueError("At coords it is not start color." + repr(coords))