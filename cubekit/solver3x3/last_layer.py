from . import BaseSolver3x3
from ..core import Cube3x3, up, Coords, FaceId, Moves, down, left, back, Position
from .solving_algos import Algo
from functools import cache

class LastLayer(BaseSolver3x3):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.side_faceids: list[FaceId] = list(
            map(lambda side_direction: Cube3x3.direction2faceId[self.start_faceid][side_direction],
                Cube3x3.side_directions)
        )
        self.connecting_side_face_coords: dict[FaceId, list[Coords]] = {
            faceid:  self.connectingCoords_withlastface(faceid) for faceid in self.side_faceids
        }
        self.last_face = self.cube.state[self.last_faceid]
        self.random_side_face = self.side_faceids[0]
    
    def prev_faceid(self, faceid: FaceId) -> FaceId:
        rotate = Cube3x3.side_directions.index(Cube3x3.faceId2direction[faceid][self.last_faceid])
        return Cube3x3.direction2faceId[faceid][Cube3x3.side_directions[(rotate+1)%4]]

    def back_faceid(self, faceid: FaceId) -> FaceId:
        return Cube3x3.direction2faceId[faceid][back]

    def connectingCoords_withlastface(self, faceid: FaceId) -> list[Coords]:
        pos: Position= Cube3x3.sideDirection2edgePosition[Cube3x3.faceId2direction[faceid][self.last_faceid]]
        if pos.x&1:
            return [Coords(faceid, x = x, y=pos.y) for x in range(self.cube.size)]
        else:
            return [Coords(faceid, x=pos.x, y=y) for y in range(self.cube.size)]
    
    # def dot2cross(self):
    #     front = self.random_side_face #random doesn't matter
    #     formula = self.cross_formula1*2 +'U' + self.cross_formula1
    #     moves = self.cube.apply_formula(front, self.last_faceid, formula)
    #     moves.comment = f"Dot before yellow Cross: {formula}"
    #     return moves
    def apply_algo(self, front: FaceId, algo) -> Moves:
        moves = self.cube.apply_formula(front, self.last_faceid, algo)
        moves.comment = f"Appling Algo ({algo.name}: {algo.value}) from FaceId: {front}."
        return moves
    
    def solve_OLL_edges(self) -> Moves:
        cross_yellow_pos: list[Position] = []
        for pos in  Cube3x3.edge_positions:
            if self.last_face.get(pos) == self.last_color:
                cross_yellow_pos.append(pos)
        if len(cross_yellow_pos) == 0:
            return self.apply_algo(self.random_side_face, Algo.OLL.Edges.dot_shape)
        elif len(cross_yellow_pos) == 4:
            return Moves([], comment="OLL of edges already done.")
        elif len(cross_yellow_pos) == 2:
            if cross_yellow_pos[0].x == cross_yellow_pos[1].x:
                return self.apply_algo(Cube3x3.direction2faceId[self.last_faceid][down], Algo.OLL.Edges.I_shape)
            elif cross_yellow_pos[0].y == cross_yellow_pos[1].y:
                return self.apply_algo(Cube3x3.direction2faceId[self.last_faceid][left], Algo.OLL.Edges.I_shape)
            else: 
                # due to order of appending in cross_yellow_pos
                if cross_yellow_pos[0] == Position(0,1) and cross_yellow_pos[1] == Position(1,0):
                    cross_yellow_pos.reverse()
                return self.apply_algo(
                    Cube3x3.EdgeOtherSide(Coords(self.last_faceid, pos=cross_yellow_pos[1])).face_id,
                    Algo.OLL.Edges.L_shape
                )
        else:
            print(f"Len {cross_yellow_pos=} is 3")
            raise NotImplementedError
    
    def solve_OLL_corners(self) -> Moves:
        side_face_with_lastcolor: dict[FaceId, list[Coords]] = dict()
        for faceid, side_coords in self.connecting_side_face_coords.items():
            sfl = side_face_with_lastcolor[faceid] = list()
            for coords in (side_coords[0], side_coords[-1]):
                if self.cube.get(coords) == self.last_color:
                    sfl.append(coords)
        lastcolor_count2faceidlist: list[list[FaceId]] = [[],[],[]]
        for faceid, color_coords in side_face_with_lastcolor.items():
            lastcolor_count2faceidlist[len(color_coords)].append(faceid)
        if lastcolor_count2faceidlist[2]:
            if len(lastcolor_count2faceidlist[2]) == 2:
                # headlight taillight case
                return self.apply_algo(
                    lastcolor_count2faceidlist[0][0], 
                    Algo.OLL.Corners.H
                )
            elif len(lastcolor_count2faceidlist[2]) == 1:
                if len(lastcolor_count2faceidlist[1]) == 0:
                    # just headlights
                    return self.apply_algo(
                        lastcolor_count2faceidlist[2][0], 
                        Algo.OLL.Corners.U
                    )
                else: #== 2
                    # headlight side light case
                    return self.apply_algo(
                        self.prev_faceid(lastcolor_count2faceidlist[2][0]), 
                        Algo.OLL.Corners.Pi
                    )
            else:
                print("lastcolor_count2faceidlist[2] lenght is", len(lastcolor_count2faceidlist[2]))
                raise Exception
        elif lastcolor_count2faceidlist[1]:
            if len(lastcolor_count2faceidlist[1]) == 3:
                if self.cube.get(self.connectingCoords_withlastface(lastcolor_count2faceidlist[1][0])[0]) == self.last_color:
                    # Sune
                    return self.apply_algo(
                        self.prev_faceid(lastcolor_count2faceidlist[0][0]), 
                        Algo.OLL.Corners.Sune
                    )
                elif self.cube.get(self.connectingCoords_withlastface(lastcolor_count2faceidlist[1][0])[-1]) == self.last_color:
                    # AntiSune
                    return self.apply_algo(
                        self.back_faceid(lastcolor_count2faceidlist[0][0]), 
                        Algo.OLL.Corners.Antisune
                    )
                else:
                    print(f"enither sune or antisune case {lastcolor_count2faceidlist=}")
                    raise Exception
            elif len(lastcolor_count2faceidlist[1]) == 2:
                if self.back_faceid(lastcolor_count2faceidlist[1][0]) == lastcolor_count2faceidlist[1][1]:
                    # side lights only, or T
                    if self.cube.get(self.connectingCoords_withlastface(lastcolor_count2faceidlist[1][0])[0]) == self.last_color:
                        faceid = lastcolor_count2faceidlist[1][1]
                    else:
                        faceid = lastcolor_count2faceidlist[1][0]
                    return self.apply_algo(
                        faceid,
                        Algo.OLL.Corners.T
                    )
                else:
                    # L
                    if self.prev_faceid(lastcolor_count2faceidlist[1][0]) == lastcolor_count2faceidlist[1][1]:
                        faceid = lastcolor_count2faceidlist[1][0]
                    else:
                        faceid = lastcolor_count2faceidlist[1][1]
                    return self.apply_algo(
                        faceid,
                        Algo.OLL.Corners.L
                    )
        elif len(lastcolor_count2faceidlist[0]) == 4:
            return Moves([], comment="OLL of corners already done.")
        raise Exception("No actual case", lastcolor_count2faceidlist)
        
    def solve_OLL(self) -> Moves:
        return self.solve_OLL_edges() + self.solve_OLL_corners()
    
    def check_OLL_edges(self) -> bool:
        for pos in Cube3x3.edge_positions:
            if self.last_face.get(pos) != self.last_color:
                return False
        return True
    
    def check_OLL_corners(self) -> bool:
        for pos in Cube3x3.corner_positions:
            if self.last_face.get(pos) != self.last_color:
                return False
        return True

    def check_OLL(self) -> bool:
        return self.check_OLL_edges() and self.check_OLL_corners()
    
    def last_face_move_postPLL(self) -> Moves:
        otherside1 = next(iter(Cube3x3.corner_other_coords(Coords(self.last_faceid, 0, 0))))
        other_colorfaceid = Cube3x3.color2faceId(self.cube.get(otherside1))
        return self.cube.apply_moves(Moves([Cube3x3.move4faceIdchange(self.last_faceid, otherside1.face_id, other_colorfaceid)],
                     comment="Matching sides post PLL."))
    
    def solve_PLL_corners_without_matching(self) -> Moves:
        correctPLLfaceid = None
        for faceid, side_coords in self.connecting_side_face_coords.items():
            if self.cube.get(side_coords[0]) == self.cube.get(side_coords[-1]):
                if correctPLLfaceid:
                    return Moves([], "PLL of corners already done.")

                else:
                    correctPLLfaceid = faceid
        if correctPLLfaceid == None:
            return self.apply_algo(self.random_side_face, Algo.PLL.Corners.none_correct)
        return self.apply_algo(self.back_faceid(correctPLLfaceid), Algo.PLL.Corners.one_pair_correct)
    
    def solve_PLL_corners(self) -> Moves:
        return self.solve_PLL_corners_without_matching() + self.last_face_move_postPLL()
    
    def solve_PLL_edges(self) -> Moves:
        correctPLLfaceid = None
        for faceid, side_coords in self.connecting_side_face_coords.items():
            if self.cube.get(side_coords[1]) == self.cube.get(side_coords[-1]):
                correctPLLfaceid = faceid
                break
        if correctPLLfaceid:
            back_faceid = self.back_faceid(correctPLLfaceid)
            color = self.cube.get(self.connecting_side_face_coords[back_faceid][1])
            color_faceid = Cube3x3.color2faceId(color)
            if back_faceid == color_faceid:
                return Moves([], "PLL of edges already done.")
            if self.prev_faceid(back_faceid) == color_faceid:
                return self.apply_algo(back_faceid, Algo.PLL.Edges.one_shiftright)
            else:
                return self.apply_algo(back_faceid, Algo.PLL.Edges.one_shiftleft)
        else:
            faceid = self.random_side_face
            color = self.cube.get(self.connecting_side_face_coords[faceid][1])
            color_faceid = Cube3x3.color2faceId(color)
            if self.back_faceid(faceid) == color_faceid:
                return self.apply_algo(faceid, Algo.PLL.Edges.none_shiftback)
            elif (prev_faceid:=self.prev_faceid(faceid)) != color_faceid:
                return self.apply_algo(faceid, Algo.PLL.Edges.none_shiftleft)
            else:
                return self.apply_algo(prev_faceid, Algo.PLL.Edges.none_shiftleft)
        raise NotImplementedError

    def solve_PLL(self) -> Moves:
        return self.solve_PLL_corners() + self.solve_PLL_edges()

    def solve_last_layer(self) -> Moves:
        return self.solve_OLL() + self.solve_PLL()


