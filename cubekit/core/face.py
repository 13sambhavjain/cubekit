# standard lib imports
import copy, warnings
# core imports
from .colors import Color, Colors
from .directions import Direction

class Position():
    """Postion on a Face"""
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __getitem__(self, index: int) -> int:
        index %= 2
        if index==1:
            return self.y
        return self.x

    def __setitem__(self, index: int, value: int) -> None:
        index %= 2
        if index==1:
            self.y = value
        else:
            self.x = value
    
    def __iter__(self):
        yield self.x
        yield self.y
    
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in vars(self).items())})'

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return NotImplemented
        return self.x == other.x and self.y == other.y

class Face:
    def __init__(self, size: int=3, fill_color: Color = None, grid: list[list[Color]] = None): #type: ignore
        """Initializes a Face object. Requires either a fill_color color (to generate a new grid)
        OR an existing grid to load from."""
        #Validation and Warnings---
        if (fill_color is None) == (grid is None):
            # If neither OR both are None
            if fill_color is not None: # Means both are NOT None (both are provided)
                warnings.warn("Both fill_color and grid are provided. Using grid.",UserWarning, stacklevel=2) # Warning case
            else: # Means both ARE None (neither provided)
                raise ValueError("Either fill_color or grid must be provided.") # Error case

        # Initialization Logic uses grid on higher priority---
        if grid is not None:
            self.grid = copy.deepcopy(grid)
        else:
            self.grid = [[fill_color for _ in range(size)] for _ in range(size)]
            
        self._size = size
            
    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, value) -> AttributeError:
        raise AttributeError('Face.size attribute is not ment to change once the Face is created.')

    def __str__(self) -> str:
        return '\n'.join(' '.join(f'{cell}' for cell in row) for row in self.grid)
    
    def __format__(self, format_spec: str) -> str:
        """
        Custom formatting using format specifiers:
        - 'i' or 'initial' or '': returns the ANSI background code with initials in them (default).
        - 'colored': returns just the background code with two spaces.
        - 'coloredinitial' or 'ci': returns just the background code with initial letter.
        - 'fullname' or 'name': returns the full name of the color.
        """
        # Use the format() function dynamically
        return '\n'.join(''.join(format(cell, format_spec) for cell in row) for row in self.grid)
    
    def rotate_clockwise(self) -> None:
        self.grid = [list(row) for row in zip(*self.grid[::-1])]

    def rotate_anticlockwise(self) -> None:
        self.grid = [list(row) for row in zip(*self.grid)][::-1]

    def rotate_180(self) -> None:
        self.grid = [row[::-1] for row in self.grid[::-1]]

    def solved(self) -> bool:
        first_color: Color = self.grid[0][0]
        return all(first_color == color for row in self.grid for color in row)
    
    def get_edge(self, direction: Direction, depth: int = 1) -> list[Color]:
        s = self.size
        if direction == Direction.up:
            return self.grid[depth - 1]
        elif direction == Direction.down:
            return self.grid[s - depth]
        elif direction == Direction.left:
            return [self.grid[i][depth - 1] for i in range(s)]
        elif direction == Direction.right:
            return [self.grid[i][s - depth] for i in range(s)]
        else:
            raise ValueError(f"Invalid direction {direction} for getting edge.")
        
    def set_edge(self, direction: Direction, colors: list[Color], depth: int = 1):
        s = self.size
        if direction == Direction.up:
            self.grid[depth - 1] = colors
        elif direction == Direction.down:
            self.grid[s - depth] = colors
        elif direction == Direction.left:
            for i in range(s):
                self.grid[i][depth - 1] = colors[i]
        elif direction == Direction.right:
            for i in range(s):
                self.grid[i][s - depth] = colors[i]
        else:
            raise ValueError(f"Invalid direction {direction} for setting edge.")
        
    def get(self, pos: Position) -> Color:
        "Given Position returns the Color at the Position in the face grid"
        return self.grid[pos.x][pos.y]
    
    def set(self, pos: Position, value: Color):
        "Given Position returns the Color at the Position in the face grid"
        self.grid[pos.x][pos.y] = value
    
    def __iter__(self):
        return iter(self.grid)
    
    def __getitem__(self, index:int) -> list[Color]:
        return self.grid[index]
    
    def __setitem__(self, index: int, value: list[Color]) -> None:
        self.grid[index] = value
    
    def __contains__(self, color: Color) -> bool:
        if isinstance(color, Color):
            for row in self.grid:
                if row.__contains__(color):
                    return True
            return False
        else:
            return self.grid.__contains__(color)
    
    def __bool__(self) -> bool:
        return bool(self.grid)
    
    def __repr__(self) -> str:
        """
        Reversible representation assuming standard construction.
        """
        # We output fill_color and size, matching the constructor signature.
        # We omit grid as it's generated automatically by __init__.
        return f'{self.__class__.__name__}(size={self.size!r}, grid={self.grid!r})'
     
FaceId = Color
FaceIds = Colors
    

if __name__ == "__main__":
    # print(Coord(Color.white, 1, 2).__repr__())
    # print(Position( 1, 2).__repr__())

    print(f'{Face(3, Color.white):name}')
        
    
