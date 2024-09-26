'''
GO TO BLOKUS_FULLER_LOGIC FOR IMPLEMENTATION OF COMPLETE GAME LOGIC
'''

"""
Fake implementations of BlokusBase.

We provide a BlokusStub implementation, and
you must provide a BlokusFake implementation.

"""
from shape_definitions import ShapeKind, definitions
from piece import Point, Shape, Piece
from base import BlokusBase, Grid
from typing import Optional


class BlokusStub(BlokusBase):
    """
    Stub implementation of BlokusBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players.
    - Only three of the 21 Blokus shapes are available:
      the one-square, two-square, and three-square straight pieces.
    - Players are allowed to place pieces in any position of the board
      they want, even if the piece collides with any squares of
      previously played pieces (squares of the new piece replace any
      conflicting ones).
    - Board positions are not validated. If a method is called with
      a position outside the board, it will likely cause an exception.
    - There is no consideration of start positions for a player's
      first move.
    - The constructor simulates two initial moves: placing
      Player 1's "1" piece in the top-left corner and
      Player 2's "2" piece in the bottom-right corner.
    - The game ends after six moves. The player, if any, who has a
      piece occupying the top-right corner of the board wins.
      Otherwise, the players tie.
    - The `remaining_shapes` method always says all three shapes remain.
    - The only shape that is considered available by `available_moves`
      is the one-square shape, and it is considered available everywhere
      on the board regardless of whether the corresponding positions are
      available or occupied.
    - Several methods return simple, unhelpful results (as opposed to
      raising NotImplementedErrors).
    """

    _shapes: dict[ShapeKind, Shape]
    _size: int
    _num_players: int
    _curr_player: int
    _grid: Grid
    _num_moves: int

    def __init__(
        self,
        num_players: int,
        size: int,
        start_positions: set[Point],
    ) -> None:
        """
        Constructor (See BlokusBase)

        This stub initializes a counter for number of moves
        in order to implement a simple game_over condition.

        Once everything is initialized, this stub implementation
        "simulates" two moves.
        """
        super().__init__(num_players, size, start_positions)
        self._shapes = self._load_shapes()
        self._size = size
        self._num_players = 2
        self._curr_player = 1
        self._grid = [[None] * size for _ in range(size)]
        self._num_moves = 0
        self._simulate_two_moves()

    def _load_shapes(self) -> dict[ShapeKind, Shape]:
        """
        Rather than reading in the representations of shapes
        from shape_definitions.py, this method manually builds
        three of the 21 kinds of shapes.

        See shape_definitions.py for more details.
        """
        # See shape_definitions.definitions[ShapeKind.ONE]
        shape_1 = Shape(ShapeKind.ONE, (0, 0), False, [(0, 0)])

        # See shape_definitions.definitions[ShapeKind.TWO]
        shape_2 = Shape(ShapeKind.TWO, (0, 0), True, [(0, 0), (0, 1)])

        # See shape_definitions.definitions[ShapeKind.THREE]
        shape_3 = Shape(
            ShapeKind.THREE, (0, 1), True, [(0, -1), (0, 0), (0, 1)]
        )

        return {
            ShapeKind.ONE: shape_1,
            ShapeKind.TWO: shape_2,
            ShapeKind.THREE: shape_3,
        }

    def _simulate_two_moves(self) -> None:
        """
        Simulates two moves:

        - Player 1 places their ShapeKind.ONE piece in the top-left corner.
        - Player 2 places their ShapeKind.TWO piece in the bottom-right corner.

        This drives the game into a state where four more pieces
        can be played before entering the game_over condition
        (six moves total).
        """
        piece_1 = Piece(self.shapes[ShapeKind.ONE])
        piece_1.set_anchor((0, 0))
        self.maybe_place(piece_1)

        # This anchor position accounts for the origin of
        # ShapeKind.TWO as specified in shape_definitions.py.
        piece_2 = Piece(self.shapes[ShapeKind.TWO])
        piece_2.set_anchor((self.size - 1, self.size - 2))
        self.maybe_place(piece_2)

    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        See BlokusBase
        """
        return self._shapes

    @property
    def size(self) -> int:
        """
        See BlokusBase
        """
        return self._size

    @property
    def start_positions(self) -> set[Point]:
        """
        See BlokusBase
        """
        return set()

    @property
    def num_players(self) -> int:
        """
        See BlokusBase
        """
        return self._num_players

    @property
    def curr_player(self) -> int:
        """
        See BlokusBase
        """
        return self._curr_player

    @property
    def retired_players(self) -> set[int]:
        """
        See BlokusBase
        """
        return set()

    @property
    def grid(self) -> Grid:
        """
        See BlokusBase
        """
        return self._grid

    @property
    def game_over(self) -> bool:
        """
        See BlokusBase
        """
        return self._num_moves == 6

    @property
    def winners(self) -> list[int]:
        """
        See BlokusBase
        """
        top_right_cell = self.grid[0][self.size - 1]
        if top_right_cell is None:
            return [1, 2]
        else:
            winner = top_right_cell[0]
            return [winner]

    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        See BlokusBase
        """
        return [ShapeKind.ONE, ShapeKind.TWO, ShapeKind.THREE]

    def any_wall_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return False

    def legal_to_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return True

    def maybe_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        for r, c in piece.squares():
            self._grid[r][c] = (self.curr_player, piece.shape.kind)
        self._curr_player = (self.curr_player % self.num_players) + 1
        self._num_moves += 1
        return True

    def retire(self) -> None:
        """
        See BlokusBase
        """
        pass

    def get_score(self, player: int) -> int:
        """
        See BlokusBase
        """
        return -999

    def available_moves(self) -> set[Piece]:
        """
        See BlokusBase
        """
        pieces = set()
        for r in range(self.size):
            for c in range(self.size):
                piece = Piece(self.shapes[ShapeKind.ONE])
                piece.set_anchor((r, c))
                pieces.add(piece)

        return pieces


#
# Your BlokusFake implementation goes here
#
"""
What still needs to be done: 
- i think game over should check if all the players have no remainingpeices,
then the game is over 

Find a way to generalize the load_shapes method--> do that in fakes, to test 
"""

class BlokusFake(BlokusBase):
    """
    Stub implementation of BlokusFake.

    This stub implementation behaves according to the following rules:

    - It only supports two players.
    - ALL 21 Blokus shapes are available
    """

    _shapes: dict[ShapeKind, Shape]
    _size: int
    _num_players: int
    _curr_player: int
    _grid: Grid
    _num_moves: int
    _retired_players: set[int]

    def __init__(
        self,
        num_players: int,
        size: int,
        start_positions: set[Point],
    ) -> None:
        """
        Constructor (See BlokusBase)

        This stub initializes a counter for number of moves
        in order to implement a simple game_over condition.

        Once everything is initialized, this stub implementation
        "simulates" two moves.

        What are the conditions of the Fake implementation?
        """
        if num_players == 1 or num_players == 2:
            self._num_players = num_players
        else:
            raise ValueError("There must be between 1 - 2 player for Blokus Fake")
        
        if size < 5: 
            raise ValueError("Grid Not appropriate size")     
        
        super().__init__(num_players, size, start_positions)
        self._shapes = self._load_shapes()
        self._size = size
        self._curr_player = 1
        self._grid = [[None] * size for _ in range(size)]
        self._num_moves = 0
        self._retired_players = set()
        self.curr_shape: Optional[str] = None
        self.curr_piece: Optional[Piece] = None


        self.player_shapes_dict: dict[int,dict[ShapeKind,Shape]] = {i+1: self.shapes 
                                for i in range(self.num_players)}
        
        self.player_used_shapes: dict[int, list[ShapeKind]] = {i+1: [] 
                                for i in range(self.num_players)}

    def _load_shapes(self) -> dict[ShapeKind, Shape]:
        """
        Uses the from_strings method in shapes to
        define all the game shapes 

        Returns, a dict of ShapeKinds as keys and the Shapes as values

        See shape_definitions.py for more details.
        """
        shape_dict: dict[ShapeKind, Shape] = {}

        for kind, string in definitions.items():
            if "O" not in string and "@" not in string: 
                transformed = False 
            else: 
                transformed = True 

            if kind == ShapeKind.Z: 
                origin = (1,1)
            else: 
                origin = (0,0)
            shape = Shape(kind,origin, transformed, []).from_string(kind,string)
            shape_dict[kind] = shape 

        return shape_dict 
      

    def _simulate_two_moves(self) -> None:
        """
        Simulates two moves:

        - Player 1 places their ShapeKind.ONE piece in the top-left corner.
        - Player 2 places their ShapeKind.TWO piece in the bottom-right corner.

        This drives the game into a state where four more pieces
        can be played before entering the game_over condition.
        """
        piece_1 = Piece(self.shapes[ShapeKind.ONE])
        piece_1.set_anchor((0, 0))
        self.maybe_place(piece_1)

        # This anchor position accounts for the origin of
        # ShapeKind.TWO as specified in shape_definitions.py.
        piece_2 = Piece(self.shapes[ShapeKind.TWO])
        piece_2.set_anchor((self.size - 1, self.size - 2))
        self.maybe_place(piece_2)

    @property
    def winners(self) -> list[int]:
        """
        See BlokusBase
        """

        players = [1,2]
        winners = []
        for player in range(self.num_players):
            player += 1
                
            score_players = self.get_score(players[0])
            player_score = self.get_score(player)
                
            if player_score > score_players:
                winners = [player]
            if player_score == score_players and player not in winners:
                winners.append(player)
        return winners 

    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        See BlokusBase
        """
        return self._shapes

    @property
    def size(self) -> int:
        """
        See BlokusBase
        """
        return self._size

    @property
    def start_positions(self) -> set[Point]:
        """
        See BlokusBase
        """
        # IDK if we need start_position yet 
        return self._start_positions

    @property
    def num_players(self) -> int:
        """
        See BlokusBase
        """
        return self._num_players

    @property
    def curr_player(self) -> int:
        """
        See BlokusBase
        """
        return self._curr_player

    @property
    def retired_players(self) -> set[int]:
        """
        See BlokusBase
        """
        return self._retired_players

    @property
    def grid(self) -> Grid:
        """
        See BlokusBase
        """
        return self._grid

    @property
    def game_over(self) -> bool:
        """
        See BlokusBase
        """
        if len(self.remaining_shapes(self.curr_player)) == 0:
            return True 
        if self.size == 48:
            return (len(self.retired_players) == self._num_players)
        
        return len(self.retired_players) == self._num_players

    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        See BlokusBase
        The number of a player's remaining shapes decrease, 
        as they their piece. 
        
        - implement this method so, it calls the player's pieces 
        and returns a list of all the pieces that they have 
        - check out piece file. 
        - -check base.py file for what methods can do 
        """
        shapes_of_player = self.player_shapes_dict[player]

        return [shape for shape in shapes_of_player.keys() 
                if shape not in self.player_used_shapes[player]] 

    def any_wall_collisions(self, piece: Piece, gui_adjust: int = 0) -> bool:
        """
        See BlokusBase

        Raises ValueError if the player has already
        played a piece with this shape.
        
        Raises ValueError if the anchor of the piece
        is None or not a valid position on the board.

        """
        if piece.anchor is None:
            raise ValueError("Piece must have an anchor")
        
        # print(self.size)
        # print(piece.squares())
        
        for r, c in piece.squares():
            if not (0  <= r < self.size 
                    and 0 <= c < self.size ):
                return True 
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        
        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None or not a valid position on the board.
    
        """
        for r,c in piece.squares():
            if self.grid[r][c] != None : 
                return True 
        if self.any_wall_collisions(piece):
            return True
        return False 
        

    def legal_to_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        
        Raises ValueError if the player has already
        played a piece with this shape.
        """
        if self.any_wall_collisions(piece) or self.any_collisions(piece):
            return False  
    
        return True

    def get_score(self, player: int) -> int:
        """
        See BlokusBase
        """
        sum_score = 0
        for each in self.remaining_shapes(player):
            sum_score += len(self._shapes[each].squares)
        return -sum_score

    def maybe_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        if not self.legal_to_place(piece):
            return False

        if piece.shape.kind in self.player_used_shapes[self.curr_player]:
            raise ValueError("Piece already used by Player")
        
        for r, c in piece.squares():
            self._grid[r][c] = (self._curr_player, piece.shape.kind)

        self.player_used_shapes[self.curr_player].append(piece.shape.kind)
    
        checking_curr = (self.curr_player % self.num_players) + 1  
        if checking_curr not in self._retired_players:
            self._curr_player = (self.curr_player % self.num_players) + 1  

        self._num_moves += 1
        return True

    def retire(self) -> None:
        """
        See BlokusBase
        """
        self.retired_players.add(self._curr_player)
        if self.curr_player % self.num_players != 0:
            self._curr_player = (self._curr_player % self.num_players) + 1 
        else:
            self._curr_player = 1


    def available_moves(self) -> set[Piece]:
        """
        Returns all legal moves for the specified player.
        """
        available_moves = set()
        remaining_shapes = self.remaining_shapes(self.curr_player)
        
        for shape_kind in remaining_shapes:
            shape = self.shapes[shape_kind]
            for r in range(self.size):
                for c in range(self.size):
                    piece = Piece(shape)
                    piece.set_anchor((r, c))
                    if self.legal_to_place(piece):
                        available_moves.add(piece)
        
        return available_moves
