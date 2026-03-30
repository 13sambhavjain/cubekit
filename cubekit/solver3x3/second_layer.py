from ..core import Cube3x3, back, Coords, FaceId, Move, Moves, Color
from . import BaseSolver3x3, FirstLayer

class SecondLayer(BaseSolver3x3):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.placed_faceId_sets: list[set[FaceId]] = list()

    def place_edge_from_bottom(self, edge_side_coords: Coords, color1_faceid: Color, color2_faceid: Color) -> Moves:
        back_faceid1 = Cube3x3.direction2faceId[color1_faceid][back]
        move1 = Cube3x3.move4faceIdchange(self.last_faceid, edge_side_coords.face_id, back_faceid1)
        move2 = Cube3x3.move4faceIdchange(color1_faceid, color2_faceid, self.last_faceid)
        move3 = Move(self.last_color, -move2.turns)
        move4 = Move(color2_faceid, -move2.turns)
        moves = Moves([move1, move2, move3, move2.unmove(), move3, move4, move3.unmove(), move4.unmove()])
        return moves
    
    def remove_edge_between(self, color1_faceid: Color, color2_faceid: Color) -> Moves:
        move2 = Cube3x3.move4faceIdchange(color1_faceid, color2_faceid, self.last_faceid)
        move3 = Move(self.last_color, -move2.turns)
        move4 = Move(color2_faceid, -move2.turns)
        moves = Moves([move2, move3, move2.unmove(), move3, move4, move3.unmove(), move4.unmove()])
        return moves
    
    # def edge_of_second_layer_between(self, faceid1: FaceId, faceid2:FaceId) -> bool:
    #     direction12 = Cube3x3.faceId2direction[faceid1][faceid2]
    #     direction21 = Cube3x3.faceId2direction[faceid2][faceid1]
    #     pos12 = Cube3x3.sideDirection2edgePosition[direction12]
    #     pos21 = Cube3x3.sideDirection2edgePosition[direction21]
    #     coords12

    def solve_second_layer(self) -> Moves:
        solution_moves = Moves([])
        last_face = self.cube.state[self.last_faceid]
        while len(self.placed_faceId_sets) < len(Cube3x3.edge_positions):
            for pos in Cube3x3.edge_positions:
                coords = Coords(self.last_faceid, pos.x, pos.y)
                color1 = last_face.get(pos)
                if color1 != self.last_color:
                    edge_side_coords = Cube3x3.EdgeOtherSide(coords)
                    color2 = self.cube.get(edge_side_coords)
                    if color2 != self.last_color:
                        faceid1 = Cube3x3.color2faceId(color1)
                        faceid2 = Cube3x3.color2faceId(color2)
                        moves = self.place_edge_from_bottom(edge_side_coords, faceid1, faceid2)
                        moves.comment = f"Found an 2nd layer edge at {coords}, placing between {faceid1} and {faceid2}"
                        self.cube.apply_moves(moves)
                        self.placed_faceId_sets.append({faceid1, faceid2})
                        solution_moves += moves
                        break #=> found and placed atleast one edge
            else:
                # for loop fully executed means no 2nd layer edge found on last layer
                # as in loop means not all edges are placed => filped or misplaced 2nd layer edges
                for direction in Cube3x3.side_directions:
                    faceid = Cube3x3.direction2faceId[self.last_faceid][direction]
                    placed: list[FaceId] = []
                    for s in self.placed_faceId_sets:
                        if faceid in s:
                            placed.append(*(s - {faceid}))
                    if len(placed) == 2:
                        continue
                    if len(placed) == 1:
                        replace_edge_faceid = Cube3x3.direction2faceId[placed[0]][back]
                    else:
                        replace_edge_faceid = Cube3x3.direction2faceId[self.last_faceid][Cube3x3.side_directions.next(direction)]
                    moves = self.remove_edge_between(faceid, replace_edge_faceid)
                    moves.comment = f"Removing wrongly placed 2nd layer edge between {faceid} and {replace_edge_faceid}"
                    self.cube.apply_moves(moves)
                    solution_moves += moves
                    break
                else:
                    raise Exception("Issue with finding unplaced edge in 2nd layer")
                # go back in the while loop to look for the removed edge piece
        return solution_moves


    
    
    

