# """
# Public API for the `core` Cube engine.

# This file defines the stable interface exposed by the core package.
# Everything imported here becomes part of the public API.
# """

# # ─────────────────────────────────────────────
# # Re-export key types
# # ─────────────────────────────────────────────

# from .colors import Color, Colors
# from .directions import Direction, SideDirections
# from .face import Face, FaceId, FaceIds
# from .coordinates import Coords, Position
# from .moves import Move, Moves
# from .cube import Cube
# from .cube_statics import CubeStatics
# from .cube_movements import CubeMovements
# from .cube3x3 import Cube3x3, Cube3x3Statics

# # ─────────────────────────────────────────────
# # Optional: Define Protocols for external use
# # ─────────────────────────────────────────────

# from typing import Protocol, Iterable


# class CubeBase(Protocol):
#     """Minimal interface all cube implementations must support."""
    
#     def get(self, coords: Coords) -> Color: ...
#     def set(self, coords: Coords, value: Color) -> None: ...
#     def apply_moves(self, moves: Moves) -> Moves: ...
#     def copy(self) -> "CubeBase": ...


# class MovableCube(CubeBase, Protocol):
#     """A Cube that can perform rotations."""
    
#     def rotate(self, face: FaceId, amount: int = 1) -> Move: ...
#     def apply_formula(self, front: FaceId, top: FaceId, *formula: str) -> Moves: ...


# class Cube3x3API(MovableCube, Protocol):
#     """Public interface for 3x3 cubes."""
    
#     @property
#     def statics(self) -> Cube3x3Statics: ...


# # ─────────────────────────────────────────────
# # What this package publicly exports
# # ─────────────────────────────────────────────

# __all__ = [
#     # primitive types
#     "Color", "Colors", "Direction", "SideDirections",
#     "Face", "FaceId", "FaceIds", "Coords", "Position",
#     "Move", "Moves",
    
#     # cube implementations
#     "Cube", "CubeStatics", "CubeMovements",
#     "Cube3x3", "Cube3x3Statics",

#     # Protocol APIs
#     "CubeBase", "MovableCube", "Cube3x3API",
# ]

# # core/api.py

# from typing import Protocol, Iterable, Union
# from core.colors import Color, Colors
# from core.directions import Direction, SideDirections
# from core.face import Face, FaceId, FaceIds
# from core.coordinates import Coords, Position
# from core.moves import Move, Moves
# from core.cube3x3 import Cube3x3
# from core.cube import Cube


# class Cube3x3API(Protocol):
#     """ Protocol for solver-facing 3×3 cube functionality. """

#     def get(self, coords: Coords) -> Color:
#         ...

#     def apply_moves(self, moves: Moves) -> Moves:
#         ...

#     def apply_formula(self, front: FaceId, top: FaceId, formula: str) -> Moves:
#         ...

#     def formula2Moves(self, front: FaceId, top: FaceId, formula: str) -> Moves:
#         ...

#     def double_rotate(self, face_id: FaceId) -> Move:
#         ...

#     @classmethod
#     def edge_coords(cls) -> Iterable[Coords]:
#         ...

#     @classmethod
#     def EdgeOtherSide(cls, coords: Coords) -> Coords:
#         ...

#     @classmethod
#     def BackEdgeCoords(cls, coords: Coords) -> Coords:
#         ...

#     @classmethod
#     def faceId2color(cls, face_id: FaceId) -> Color:
#         ...

#     @classmethod
#     def color2faceId(cls, color: Color) -> FaceId:
#         ...

#     @classmethod
#     def move4faceIdchange(cls, from_face: FaceId, to_face: FaceId, target_face: FaceId) -> Move:
#         ...

#     @classmethod
#     def turns4faceIdchange(
#         cls, start_face: FaceId, current_face: FaceId, target_face: FaceId
#     ) -> int:
#         ...


# # Public API export
# __all__ = [
#     "Color",
#     "Colors",
#     "Direction",
#     "SideDirections",
#     "Face",
#     "FaceId",
#     "FaceIds",
#     "Coords",
#     "Position",
#     "Move",
#     "Moves",
#     "Cube",
#     "Cube3x3",
#     "Cube3x3API",
# ]
