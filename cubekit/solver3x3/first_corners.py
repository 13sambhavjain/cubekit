from ..core import Cube3x3, back, Coords, FaceId, Move, Moves, Color
from .base_solver3x3 import BaseSolver3x3

class FirstCorners(BaseSolver3x3):
    def __init__(self, *args, **kwargs) ->  None: 
        super().__init__(*args, **kwargs)
        self.placed_corner_positions: list[set[Color]] = list()
    
    def startcorner_on_startface(self, coords: Coords, check: bool=False) -> Moves:
        if check:
            self.checkRaise_start_color_on_startface_coords(coords)
        otherSide1, otherSide2 = Cube3x3.corner_other_coords(coords)
        otherColor1, otherColor2 = self.cube.get(otherSide1), self.cube.get(otherSide2)
        otherColor1_faceid = Cube3x3.color2faceId(otherColor1)
        otherColor2_faceid = Cube3x3.color2faceId(otherColor2)
        def moves4moving_wrong_start_corner_by2position():
            turning_faceid = otherSide1.face_id
            back_faceid = Cube3x3.direction2faceId[turning_faceid][back]
            move = Cube3x3.move4faceIdchange(
                turning_faceid,
                self.start_faceid,
                otherSide2.face_id
            )
            move2 = Move(back_faceid, move.turns)
            return Moves(
                [move, move2, Move(self.last_faceid, 2), move2.unmove(), move.unmove()],
                comment=f"Removing wrong start corner form {coords}, placing it correctly."
            )
        def moves4moving_wrong_start_corner_by1position(
                uncommon_otherside_faceid, commonface_faceid) -> Moves:
            turns = Cube3x3.turns4faceIdchange(uncommon_otherside_faceid, self.start_faceid, commonface_faceid) # 3 or 1
            move1 = Move(uncommon_otherside_faceid, turns)
            move2 = Move(commonface_faceid, turns)
            return Moves(
                [move1, Move(self.last_faceid, 2), move1.unmove(), 
                move2, Move(self.last_faceid, -turns), move2.unmove()],
                comment=f"removing wrong start corner form {coords}, placing it correctly."
            )
        if otherSide1.face_id == otherColor1_faceid: #no need to check color2
            if {otherColor1, otherColor2} not in self.placed_corner_positions:
                moves = Moves(comment=f"Start Corner {coords} is already placed.")
            else:
                return Moves([])

        elif otherSide1.face_id == otherColor2_faceid: #as never possible for turning_faceid == 
            moves = moves4moving_wrong_start_corner_by1position(
                otherSide2.face_id, otherSide1.face_id)
        elif otherSide2.face_id == otherColor1_faceid: # so only 3 checks => 4 possible cases 
            moves = moves4moving_wrong_start_corner_by1position(
                otherSide1.face_id, otherSide2.face_id)
        else: #means replace with same start face opposite corner position
            moves = moves4moving_wrong_start_corner_by2position()

        self.cube.apply_moves(moves)
        self.placed_corner_positions.append({otherColor1, otherColor2})
        return moves
            
    def startcorner_on_lastface(self, coords: Coords, check: bool=False) -> Moves:
        if check:
            self.checkRaise_start_color_on_lastface_coords(coords)
        otherSide1, otherSide2 = Cube3x3.corner_other_coords(coords)
        otherColor1, otherColor2 = self.cube.get(otherSide1), self.cube.get(otherSide2)
        otherColor1_faceid = Cube3x3.color2faceId(otherColor1)
        otherColor2_faceid = Cube3x3.color2faceId(otherColor2)
        move2below = Cube3x3.move4faceIdchange(self.last_faceid, otherSide1.face_id, otherColor2_faceid) # will always be opposite match of colors
        # coords changed so otherSide is not valid anymore
        turn = Cube3x3.turns4faceIdchange(otherColor1_faceid, self.start_faceid, otherColor2_faceid) # 1 or 3
        move2sidelower = Move(otherColor1_faceid, turn)
        move2shiftout = Move(self.last_faceid, -turn) #need to unmove previous move
        # currently on side lower exact opposite to actual place in cube
        move2bring_down = Move(otherColor2_faceid, -turn)
        move2shiftin = Move(self.last_faceid, 2) #need to unmove previous move
        moves = Moves(
            [move2below, move2sidelower, move2shiftout, move2sidelower.unmove(),
             move2bring_down, move2shiftin, move2bring_down.unmove()],
            comment=f"Correctly placing Corner from below at {coords} to right place."
        )
        self.cube.apply_moves(moves)
        self.placed_corner_positions.append({otherColor1, otherColor2})
        return moves
    
    def startcorner_on_sideface(self, coords: Coords, check: bool=False) -> Moves:
        if check:
            self.checkRaise_start_color_on_sideface_coords(coords)
        otherSide1, otherSide2 = Cube3x3.corner_other_coords(coords)
        otherColor1, otherColor2 = self.cube.get(otherSide1), self.cube.get(otherSide2)
        otherColor1_faceid = Cube3x3.color2faceId(otherColor1)
        otherColor2_faceid = Cube3x3.color2faceId(otherColor2)
        def color_on_side_top() -> Moves:
            # similar cases to startcorner on startface but wrongly placed
            # otherside 1 is start color
            move1 = Cube3x3.move4faceIdchange(coords.face_id, self.start_faceid, otherSide2.face_id)
            turn = move1.turns
            if otherColor2_faceid == otherSide2.face_id:
                #means the other othercolor1faceid wont be coords.faceid
                #shortcut m f m'  (need to implement m for this in moves/formula)
                move2 = Move(otherColor1_faceid, -turn)
                move3 = Move(self.last_faceid, turn)
                moves = Moves([move1, move2, move3, move2.unmove(), move1.unmove()])
            elif otherColor2_faceid == coords.face_id:
                #means othercolor1_faceid == otherSide2.faceid
                # means correct place of corner but wrong orientation
                move2 = Move(self.last_faceid, 2)
                move3 = Move(otherColor1_faceid, -turn)
                moves = Moves([move1, move2, move1.unmove(), move3, move2, move3.unmove()])
            elif otherColor1_faceid == coords.face_id:
                move2 = Move(self.last_faceid, 2)
                move3 = Move(coords.face_id, 2)
                move4 = Move(self.last_faceid, turn)
                moves = Moves([move1, move2, move3, move4, move1])
            else:
                move2 = Move(otherColor1_faceid, -turn)
                move3 = Move(self.last_faceid, 2)
                moves = Moves([move1, move2, move3, move2.unmove(), move1.unmove()])
            moves.comment = f"Correctly placing start corner from side top at {coords}."
            return moves
                
        def color_on_side_bottom() -> Moves:
            # otherSide1.faceid == self.lastfaceid
            # similar cases to startcorner on startface but wrongly placed
            move1 = Cube3x3.move4faceIdchange(self.last_faceid, otherSide2.face_id, otherColor1_faceid)
            move2 = Cube3x3.move4faceIdchange(otherColor2_faceid, self.start_faceid, otherColor1_faceid)
            move3 = Cube3x3.move4faceIdchange(self.last_faceid, otherColor1_faceid, otherColor2_faceid)
            moves = Moves([move1, move2, move3, move2.unmove()])
            moves.comment = f"Correctly placing start corner from side botton at {coords}."
            return moves
        
        def swap_other1_other2_nonlocal():
            nonlocal otherSide1, otherSide2, otherColor1, otherColor2
            nonlocal otherColor1_faceid, otherColor2_faceid
            otherSide1, otherSide2 = otherSide2, otherSide1
            otherColor1, otherColor2 = otherColor2, otherColor1
            otherColor1_faceid, otherColor2_faceid = otherColor2_faceid, otherColor1_faceid

        if otherSide2.face_id == self.start_faceid or otherSide2.face_id == self.last_faceid:
            swap_other1_other2_nonlocal()

        if otherSide1.face_id == self.start_faceid:
            moves = color_on_side_top()
        elif otherSide1.face_id == self.last_faceid:
            moves = color_on_side_bottom()
        else:
            raise ValueError(f"Setting or swaping of variables went wrong.")
        self.cube.apply_moves(moves)
        self.placed_corner_positions.append({otherColor1, otherColor2})
        return moves
     
    def solve_first_corners(self) -> Moves:
        first_corners_moves = Moves()
        for search in range(2*len(Cube3x3.corner_positions)): #assuming will atleast solve one corner every two iteration
            for coords in Cube3x3.corner_coords():
                if self.cube.get(coords) == self.start_color:
                    if coords.face_id == self.start_faceid:
                        first_corners_moves += self.startcorner_on_startface(coords)
                    elif coords.face_id == self.last_faceid:
                        first_corners_moves += self.startcorner_on_lastface(coords)
                    else:
                        first_corners_moves += self.startcorner_on_sideface(coords)
                    if len(self.placed_corner_positions) == len(Cube3x3.corner_positions):
                        return first_corners_moves
        else:
            raise Exception(f"even after {search} searches on corners not able to solve, check logic")
    
    def check_first_corners(self) -> bool:
        face = self.cube.state[self.start_faceid]
        for position in self.cube.corner_positions:
            if face.get(position) != self.start_color:
                return False
        return True