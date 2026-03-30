# standard lib imports
from enum import StrEnum, auto

class Direction(StrEnum):
    front = auto()
    back = auto()
    left = auto()
    right = auto()
    up = auto()
    down = auto()
    def __repr__(self):
        # Returns a string that looks like "Direction.<DirectionName>"
        return f"{self.__class__.__name__}.{self.name}"

class SideDirections():
    """A collection of Side Directions with cyclic indexing and iteration."""
    _sideDirections = [Direction.up, Direction.right, Direction.down, Direction.left]
    _instance = None

    def __new__(cls):
        """Singleton pattern to ensure only one instance of SideDirections exists."""
        if cls._instance is None:
            cls._instance = super(SideDirections, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, *args, **kwargs):
        """
        Flexible initializer that accepts any arguments.
        It doesn't actually use args/kwargs for anything in this specific setup,
        but it makes the class definition resilient to being called with arguments.
        """
        pass
    
    def __iter__(self):
        """Allow iteration: for direction in SideDirections"""
        return iter(self._sideDirections)

    def __getitem__(self, index: int) -> Direction:
        """Allow cyclic indexing: sideDirections[n] wraps around."""
        return self._sideDirections[index % len(self._sideDirections)]
    
    def __contains__(self, direction: Direction) -> bool:
        """Check if a direction is a side direction."""
        return direction in self._sideDirections

    def __len__(self) -> int:
        """Number of side directions."""
        return len(self._sideDirections)

    def index(self, direction: Direction) -> int:
        """Return the index of a given direction."""
        return self._sideDirections.index(direction)

    def next(self, direction: Direction) -> Direction:
        """Return the next side direction cyclically."""
        i = self._sideDirections.index(direction)
        if i == -1:
            raise ValueError(f"{direction} not in SideDirections")
        return self._sideDirections[(i + 1) % len(self._sideDirections)]

    def prev(self, direction: Direction) -> Direction:
        """Return the previous side direction cyclically."""
        i = self._sideDirections.index(direction)
        if i == -1:
            raise ValueError(f"{direction} not in SideDirections")
        return self._sideDirections[(i - 1) % len(self._sideDirections)]

    def __str__(self):
        """String representation of the SideDirections collection."""
        return f"SideDirections({', '.join(c.name for c in self._sideDirections)})"
    
    def __repr__(self):
        """Official string representation of the SideDirections collection."""
        return f'SideDirections(_sideDirections={self._sideDirections})'


if __name__ == "__main__":
    colors = SideDirections()
    print(repr(colors))
    # print(colors[0])
    # for color in colors:
    #     print(color)
    # print(colors.next(Direction.right))
    # print(colors.prev(Direction.up))
    # print(colors.index(Direction.down))
    # print(len(colors))
    # print(colors.__repr__())
    pass