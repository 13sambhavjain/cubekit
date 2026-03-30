#  standard lib imports
from copy import deepcopy
# core imports
from .face import FaceId

class Move():
    def __init__(self, faceId: FaceId, turns: int=1):
        self.faceId: FaceId = faceId
        self._turns: int = turns%4
    
    @property
    def turns(self) -> int:
        return self._turns
    @turns.setter
    def turns(self, value: int) -> None:
        self._turns = value % 4

    def unmove(self) -> Move:
        return Move(self.faceId, -self.turns)
    
    def __str__(self) -> str:
        face_letter: str = self.faceId.__format__('i').strip()
        if self.turns == 0:
            return ""
        elif self.turns == 1:
            return f'{face_letter}'
        elif self.turns == 2:
            return f'{face_letter}\u00b2'
        elif self.turns == 3:
            return f'{face_letter}`'
        else:
            raise ValueError(f"Invalid number of turns, {self.__repr__()}")
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(faceId={self.faceId!r}, turns={self.turns!r})'
    
    def __bool__(self) -> bool:
        return self.turns != 0
    
    def __add__(self, other: Move) -> Move|Moves:
        if self.faceId == other.faceId:
            return Move(self.faceId, self.turns + other.turns)
        else:
            return Moves([self, other])
        
    def __radd__(self, other: Moves) -> Moves:
        # raise NotImplementedError
        if not isinstance(other, Moves):
            raise TypeError(f"Unsupported operand type(s) for +: '{type(other
                                                                        ).__name__}' and '{type(self).__name__}'")
        otherCopy = deepcopy(other)
        while self.faceId == otherCopy[0].faceId:
            t = otherCopy[0].turns + self.turns
            if t % 4 == 0:
                otherCopy.pop(0)
            else:
                otherCopy[0].turns = t % 4
            self.turns = 0
        if self:
            otherCopy.insert(0, self)
        return otherCopy
    
    # currently unused
    # def __iter__(self):
    #     yield self.faceId
    #     yield self.turns

    # def __getitem__(self, index: int) -> FaceId|int:
    #     index %= 2
    #     if index==0:
    #         return self.faceId
    #     return self.turns
    
    # def __setitem__(self, index: int, value: FaceId|int) -> None:
    #     index %= 2
    #     if index==0:
    #         self.faceId = value  # type: ignore
    #     else:
    #         self.turns = value  # type: ignore

class Moves():
    def __init__(self, moves: list[Move] = None, comment:str = '', efficient: bool = False): #type: ignore
        self.moves: list[Move] = moves if moves is not None else list()
        self.efficient: bool = efficient
        self.comment: str = comment

    def append(self, move: Move) -> None:
        if not move:
            return
        if self.efficient and self.moves and self.moves[-1].faceId == move.faceId:
            combined_turns = (self.moves[-1].turns + move.turns) % 4
            if combined_turns == 0:
                self.moves.pop()
            else:
                self.moves[-1].turns = combined_turns
        else:
            self.moves.append(move)

    def make_efficient(self) -> None:
        # efficient_moves = Moves(efficient=True)
        # for move in self.moves:
        #     efficient_moves.append(move)
        # self.moves = efficient_moves.moves
        # self.efficient = True
        pass 

    def extend(self, moves: Moves) -> None:
        if self.efficient:
            for move in moves:
                self.append(move)
        else:
            self.moves.extend(moves.moves)

    def insert(self, index: int, move: Move, efficient: bool = True) -> None:
        if self.efficient:
            raise NotImplementedError
        else:
            self.moves.insert(index, move)

    def __add__(self, other: Move|Moves) -> Moves:
        result = deepcopy(self)
        if isinstance(other, Move):
            result.append(other)
        elif isinstance(other, Moves):
            for move in other:
                result.append(move)
            result.efficient = self.efficient and other.efficient
            result.comment = self.comment + ('\n' if other.comment else "" )+ other.comment
        return result
    
    def __str__(self) -> str:
        return ' '.join(str(move) for move in self.moves)

    def pop(self, index: int = -1) -> Move:
        if self.efficient and index != -1:
            raise NotImplementedError
        return self.moves.pop(index)

    def __len__(self) -> int:
        return len(self.moves)
    
    def __getitem__(self, index: int) -> Move:
        return self.moves[index]
    
    def __setitem__(self, index: int, move: Move) -> None:
        self.moves[index] = move

    def __delitem__(self, index: int) -> None:
        del self.moves[index]

    def __iter__(self):
        return iter(self.moves)
    
    def __repr__(self) -> str:
        return f'Moves(moves={self.moves}, comment={self.comment}, efficient={self.efficient})'

    def __contains__(self, move: Move) -> bool:
        return move in self.moves
    
    def __bool__(self) -> bool:
        return bool(self.moves)

