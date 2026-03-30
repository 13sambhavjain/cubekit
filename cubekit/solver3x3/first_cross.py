from ..core import Cube3x3, back, Coords, FaceId, Move, Moves, Color
from .base_solver3x3 import BaseSolver3x3
class FirstCross(BaseSolver3x3):
    def __init__(self, *args, **kwargs) ->  None: 
        super().__init__(*args, **kwargs)
        self.placed_edge_colors: set = set()
    
    def _edge_on_top(self, coords: Coords, check: bool=False) -> Moves:
        if check:
            self.checkRaise_start_color_on_startface_coords(coords)
        otherSide = Cube3x3.EdgeOtherSide(coords)
        otherColor = self.cube.get(otherSide)

        if Cube3x3.faceId2color(otherSide.face_id) == otherColor:
            self.placed_edge_colors.add(otherColor)
            return Moves(comment=f"{coords} is already placed.")
        
        if len(self.placed_edge_colors) == 0:
            # rotate color logic
            otherColor_faceId = Cube3x3.color2faceId(otherColor)
            moves = Moves([Cube3x3.move4faceIdchange(self.start_faceid, otherSide.face_id, otherColor_faceId)])
            self.cube.apply_moves(moves)
            self.placed_edge_colors.add(otherColor)
            return moves
        else: 
            """ ***Improvement: some are already placed, but this is wrongly placed. should try to fit others first....Do this only if one more is stuck at wrong place, even when you do this should put it to side only not bottom."""
            new_coords = Cube3x3.BackEdgeCoords(coords)
            moves = Moves(
                moves=[self.cube.double_rotate(otherSide.face_id)], 
                comment=f"Putting the wrongply paced {self.start_color=} with the last color."
            ) + self._edge_on_bottom(new_coords) # color on bottom places the edge in set
            # already applying moves in double rotate and color_on bottom
            return moves
    
    def _edge_on_bottom(self, coords: Coords, check: bool=False) -> Moves:
        if check:
            self.checkRaise_start_color_on_lastface_coords(coords)

        otherSide = Cube3x3.EdgeOtherSide(coords)
        otherColor = self.cube.get(otherSide)
        otherColor_faceId = Cube3x3.color2faceId(otherColor)
        moves =  Moves(
            moves=[Cube3x3.move4faceIdchange(self.last_faceid, otherSide.face_id, otherColor_faceId), 
                    Move(otherColor, 2)], 
            comment=f"Placed c{repr(coords)}"
        )
        self.cube.apply_moves(moves)
        self.placed_edge_colors.add(otherColor)
        return moves
    
    def _edge_on_side(self, coords: Coords, check: bool=False) -> Moves:
        if check:
            self.checkRaise_start_color_on_sideface_coords(coords)
        otherSide = Cube3x3.EdgeOtherSide(coords)
        otherColor = self.cube.get(otherSide)
        otherColor_faceId = Cube3x3.color2faceId(otherColor)
        def color_on_side_top() -> Moves:
            turns = Cube3x3.turns4faceIdchange(self.start_faceid, coords.face_id, otherColor_faceId)
            if turns == 3:
                moves = self.cube.apply_formula(coords.face_id, self.start_faceid, 'FR')
            elif turns == 2:
                moves = self.cube.apply_formula(coords.face_id, self.start_faceid, 'FURU`')
            elif turns == 1:
                moves = self.cube.apply_formula(coords.face_id, self.start_faceid, 'F`L`')
            else: # turns == 0:
                moves = self.cube.apply_formula(coords.face_id, self.start_faceid, 'FU`RU')
            moves.comment = f"First Edge Color on Side top, {coords=}, shifting from Face={otherSide.face_id} to Face={otherColor_faceId}"
            self.placed_edge_colors.add(otherColor)
            return moves
        
        def color_on_side_mid() -> Moves:
            moves = Moves([
                Cube3x3.move4faceIdchange(self.start_faceid, otherColor_faceId, otherSide.face_id),
                Cube3x3.move4faceIdchange(otherSide.face_id, coords.face_id, self.start_faceid),
                Cube3x3.move4faceIdchange(self.start_faceid, otherSide.face_id, otherColor_faceId)
            ])
            moves.comment = f"First Edge Color on Side mid, {coords=}, shifting from Face={otherSide.face_id} to Face={otherColor_faceId}"
            self.cube.apply_moves(moves)
            self.placed_edge_colors.add(otherColor)
            return moves
        
        def color_on_side_bottom() -> Moves:
            if otherColor_faceId == coords.face_id: #edge of same face
                return self.cube.apply_formula(coords.face_id, self.start_faceid, 'F`U`RU')
            elif otherColor_faceId == Cube3x3.direction2faceId[coords.face_id][back]: #edge of back face
                moves = self.cube.formula2Moves(coords.face_id, self.start_faceid, 'F`URU`')
            else: #edge of either of side faces
                moves = Moves([
                    Cube3x3.move4faceIdchange(coords.face_id, self.last_faceid, otherColor_faceId),
                    Cube3x3.move4faceIdchange(otherColor_faceId, coords.face_id, self.start_faceid)
                ])

            moves.comment = f"First Edge Color on Side bottom, {coords=}, shifting from Face={otherSide.face_id} to Face={otherColor_faceId}."
            if Cube3x3.faceId2color(coords.face_id) in self.placed_edge_colors: # only for edge of side or back faces
                moves.append(moves[0].unmove())
                moves.comment += " Moved a placed edge, so putting it back in last move."
            self.cube.apply_moves(moves)
            self.placed_edge_colors.add(otherColor)
            return moves

        if otherSide.face_id == self.start_faceid:
            return color_on_side_top()
        elif otherSide.face_id == self.last_faceid:
            return color_on_side_bottom()
        else:
            return color_on_side_mid()
     
    def solve_first_cross(self) -> Moves:
        first_cross_moves = Moves()
        for search in range(2*len(Cube3x3.edge_positions)): #assuming will atleast solve one edge every two iteration
            for coords in Cube3x3.edge_coords():
                if self.cube.get(coords) == self.start_color:
                    if coords.face_id == self.start_faceid:
                        first_cross_moves += self._edge_on_top(coords)
                    elif coords.face_id == self.last_faceid:
                        first_cross_moves += self._edge_on_bottom(coords)
                    else:
                        first_cross_moves += self._edge_on_side(coords)
                    if len(self.placed_edge_colors) == len(Cube3x3.edge_positions):
                        return first_cross_moves
        else:
            raise Exception(f"even after {search} searches on edges not able to solve, check logic")
