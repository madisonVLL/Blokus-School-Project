"""
Blokus shapes and pieces.
"""
import copy
from typing import *
import textwrap

from shape_definitions import ShapeKind

Point = tuple[int, int]

def row(point: Point) -> int:
    return point[0]


def col(point: Point) -> int:
    return point[1]


class Shape:
    """
    Representing the 21 Blokus shapes, as named and defined by
    the string representations in shape_definitions.py.

    The locations of the squares are relative to the origin.

    The can_be_transformed boolean indicates whether or not
    the origin was explicitly defined in the string
    representation of the shape.

    See shape_definitions.py for more details.
    """

    kind: ShapeKind
    origin: Point
    can_be_transformed: bool
    squares: list[Point]

    def __init__(
        self,
        kind: ShapeKind,
        origin: Point,
        can_be_transformed: bool,
        squares: list[Point],
    ) -> None:
        """
        Constructor
        """
        self.kind = kind
        self.origin = origin
        self.can_be_transformed = can_be_transformed
        self.squares = squares

    def __str__(self) -> str:
        """
        Returns a complete string representation of the
        shape.
        """
        return f"""
            Shape
                kind = {self.kind}
                origin = {self.origin}
                can_be_transformed = {self.can_be_transformed}
                squares = {list(map(str, self.squares))}
        """

    @staticmethod
    def from_string(kind: ShapeKind, definition: str) -> "Shape":
        """
        Create a Shape based on its string representation
        in shape_definitions.py. See that file for details.
        """
        def_list = list(textwrap.dedent(definition))
        def_list.pop(0)
        transform = False
        shape_locations = []
        origin = (0,0)

        current_row = 0
        current_cell = 0
        for character in def_list:
            if character == ' ':
                current_cell += 1
            if character == '\n':
                current_row += 1
                current_cell = 0
            if character == 'X':
                shape_locations.append((current_row, current_cell))
                current_cell += 1
            if character == 'O':
                origin = (current_row, current_cell)
                shape_locations.append((current_row, current_cell))
                current_cell += 1
            if character  == '@':
                origin = (current_row, current_cell)
                current_cell += 1
        
        if "@" in def_list or "O" in def_list: 
            transform = True

        new_y, new_x = (0,0)
        origin_r, origin_c = origin  
        
        if origin_r > 0:
            new_y = -origin_r 
        if origin_r < 0:
            new_y = origin_r 
        if origin_c > 0:
            new_x = -origin_c
        if origin_c < 0:
            new_x = origin_c
        
        for i, point in enumerate(shape_locations):
            r, c = point
            shape_locations[i] = (r + new_y, c + new_x)
  
        return Shape(kind, origin, transform, shape_locations)
    

    def flip_horizontally(self) -> None:
        """
        Flip the shape horizontally
        (across the vertical axis through its origin),
        by modifying the squares in place.
        """
        for i, square in enumerate(self.squares):
            y, x = square
            self.squares[i] = (-y, x)

    def rotate_left(self) -> None:
        """
        Rotate the shape left by 90 degrees,
        by modifying the squares in place.
        """
        
        for i, square in enumerate(self.squares):
            y, x = square
            self.squares[i] = (-x, y)

    def rotate_right(self) -> None:
        """
        Rotate the shape right by 90 degrees,
        by modifying the squares in place.
        """
        for i, square in enumerate(self.squares):
            y, x = square
            self.squares[i] = (x, -y)

class Piece:
    """
    A Piece takes a Shape and orients it on the board.

    The anchor point is used to locate the Shape.

    For flips and rotations, rather than storing these
    orientations directly (for example, using two attributes
    called face_up: bool and rotation: int), we modify
    the shape attribute in place. Therefore, it is important
    that each Piece object has its own deep copy of a
    Shape, so that transforming one Piece does not affect
    other Pieces that have the same Shape.
    """

    shape: Shape
    anchor: Optional[Point]

    def __init__(self, shape: Shape, face_up: bool = True, rotation: int = 0):
        """
        Each Piece will get its own deep copy of the given shape
        subject to initial transformations according to the arguments:

            face_up:  If true, the initial Shape will be flipped
                      horizontally.
            rotation: This number, modulo 4, indicates how many
                      times the shape should be right-rotated by
                      90 degrees.
        """
        # Deep copy shape, so that it can be transformed in place
        self.shape = copy.deepcopy(shape)

        # The anchor will be set by set_anchor
        self.anchor = None

        # We choose to flip...
        if not face_up:
            self.shape.flip_horizontally()

        # ... before rotating
        for _ in range(rotation % 4):
            self.shape.rotate_right()

    def set_anchor(self, anchor: Point) -> None:
        """
        Set the anchor point.
        """
        self.anchor = anchor

    def _check_anchor(self) -> None:
        """
        Raises ValueError if anchor is not set.
        Used by the flip and rotate methods below,
        so each of those may raise ValueError.
        """
        if self.anchor is None:
            raise ValueError(f"Piece does not have anchor: {self.shape}")

    def flip_horizontally(self) -> None:
        """
        Flip the piece horizontally.
        """
        self._check_anchor()
        self.shape.flip_horizontally()

    def rotate_left(self) -> None:
        """
        Rotate the shape left by 90 degrees,
        by modifying the squares in place.
        """
        self._check_anchor()
        self.shape.rotate_left()

    def rotate_right(self) -> None:
        """
        Rotate the shape right by 90 degrees,
        by modifying the squares in place.
        """
        self._check_anchor()
        self.shape.rotate_right()

    def squares(self) -> list[Point]:
        """
        Returns the list of points corresponding to the
        current position and orientation of the piece.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()
        assert self.anchor is not None
        return [
            (row(self.anchor) + r, col(self.anchor) + c)
            for r, c in self.shape.squares
        ]

    
    def cardinal_neighbors(self) -> set[Point]:
        """
        Returns the combined cardinal neighbors
        (north, south, east, and west)
        corresponding to all of the piece's squares.

        Raises ValueError if anchor is not set.
        """
        if self.anchor == None:
            raise ValueError("There is no anchor for this shape")
        cardinal_pieces = set()
        for square in self.squares():
            y, x = square
            cardinal_pieces.add((max(y-1, 0), x))
            cardinal_pieces.add((y, max( x - 1 , 0)))
            cardinal_pieces.add((y, x+1))
            cardinal_pieces.add((y+1,x))
        
        return set(filter(lambda x: x not in self.squares(), cardinal_pieces))
    
    def intercardinal_neighbors(self) -> set[Point]:
        '''
        Returns the combined intercardinal neighbors
        (northeast, southeast, southwest, and northwest)
        corresponding to all of the piece's squares.

        Raises ValueError if anchor is not set.
        '''
        if self.anchor == None:
            raise ValueError("There is no anchor for this shape")
        
        diagnols = set()

        for point in self.squares():
            r, c = point
            diagnol_pieces = {(r - 1, c - 1), (r + 1, c + 1), (r + 1, c - 1), (r - 1, c + 1)}
            diagnols.update(diagnol_pieces)

        not_in_squares = set(filter(lambda x: x not in self.squares(), diagnols))
        
        return set(filter(lambda x: x not in self.cardinal_neighbors(), not_in_squares))

        
            
                
