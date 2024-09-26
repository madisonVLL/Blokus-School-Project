from typing import Optional, Callable
from shape_definitions import ShapeKind, definitions
from piece import Point, Shape, Piece
from base import BlokusBase, Grid

class Blokus(BlokusBase):
    """
    Class for the Blokus Game
    """
    def __init__(self, num_player: int, size: int,
                 start_positions: set[Point]) -> None:
        """
        See BlokusBase 
        """

        super().__init__(num_player, size, start_positions)
        self._shapes = self._load_shapes()
        self._curr_player: int = 1
        self._grid:list[list[tuple[int, ShapeKind]]] = [[None] *
                                                        size for _ in range(size)]
        self._num_moves: int = 0
        self._retired_players:set[int]= set()
        self.curr_shape: Optional[str] = None
        self.curr_piece: Optional[Piece] = None

        if self.num_players == 0:
            raise ValueError("Invalid number of players")

        if self.size < 5:
            raise ValueError("Invalid board size")

        if len(self.start_positions) < self.num_players:
            raise ValueError("Not enough starting positions for the number of players")

        for start in self.start_positions:
            r, c = start
            check: Callable = lambda x: x < self.size-1 or x > 0
            if not (check(r) or check(c)):
                raise ValueError("Invalid starting positions")

        self.player_shapes_dict: dict[int,dict[ShapeKind,Shape]] = {i+1: self.shapes
                                for i in range(self.num_players)}

        self.player_used_shapes: dict[int, list[ShapeKind]] = {i+1: []
                                for i in range(self.num_players)}

    def _load_shapes(self) -> dict[ShapeKind, Shape]:
        """
        Loading all the shapes possible for the blokus game 
        
        Returns a dictionary with Shapekinds, shape: dict[ShapeKind,Shape]
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

    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        See BlokusBase 

        See shape_definitions.py for more details.
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
    def curr_player_shapes(self) -> dict[ShapeKind, Shape]:
        """
        Returns all the remaining shapes of the current player 
        
        Returns a dict of Shapekinds as keys, and shapes as values
        """
        return self.player_shapes_dict[self.curr_player]

    @property
    def game_over(self) -> bool:
        """
        See BlokusBase

        Additional functionality is, game is over when there's 
        no more empty positions on the board. 
        """
        check = (len(self.retired_players) == self._num_players)

        return check or self.all_pieces_played or not self.fllled_board

    @property
    def winners(self) -> list[int]:
        """
        See BlokusBase 
        """
        scores = {player: self.get_score(player) for
                  player in range(1, self.num_players + 1)}

        max_score = max(scores.values())

        winners = [player for player, score in
                   scores.items() if score == max_score]
        return winners

    @property
    def num_moves(self) -> int:
        return self._num_moves

    @property
    def all_pieces_played(self) -> bool:
        '''
        Returns true if all players have played all their pieces
        
        Inputs:
        self -> specifically num_players and remaining shapes
        
        Returns:
            bool -> True if all players have played all their pieces
        '''

        is_over: list[bool] = []
        for i in range(self.num_players):
            if len(self.player_used_shapes[i+1]) == 21:
                is_over.append(True)

        return len(is_over) == self.num_players

    @property
    def fllled_board(self) -> bool:
        """
        In the very small likelyhood that players fill the board, this 
        function will return True. 

        Returns, a bool 
        """

        for iy,_ in enumerate(self.grid):
            for ix,_ in enumerate(self.grid):
                if self.grid[iy][ix] == None:
                    return True
        return False

    #
    # METHODS
    #

    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        See BlokusBase 
        """
        shapes_of_player = self.player_shapes_dict[player]

        return [shape for shape in shapes_of_player.keys()
                if shape not in self.player_used_shapes[player]]

    def any_wall_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        if piece.anchor is None:
            raise ValueError("Piece must have an anchor")

        for r, c in piece.squares():
            if not (0 <= r < self.size and 0 <= c < self.size):
                return True
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        See BlockusBase 

        Additionally, function returns true if the intercardinal position 
        IS NOT a piece placed by the current player, False otherwise. 
        """

        for r,c in piece.squares():
            if self.grid[r][c] != None:
                return True

        for r, c in piece.cardinal_neighbors():
            if r in range(0, self.size) and c in range(0, self.size):
                if self.grid[r][c] is not None:
                    if self.grid[r][c][0] == self.curr_player:
                        return True

        if self.num_moves >= self.num_players:
            for r, c in piece.intercardinal_neighbors():
                if r in range(0, self.size) and c in range(0, self.size):
                    if self.grid[r][c] is not None:
                        if self.grid[r][c][0] == self.curr_player:
                            return False
            return True
        return False

    def legal_to_place(self, piece: Piece) -> bool:
        """
        See BlokusBase 

        New Functionality: 
        Checks if the piece is on a starting position when the 
        game start. In addition to the other conditions, returns 
        False if its not on a start position

        Input: 
            piece, a Piece 

        Returns, a bool 
        """

        on_start = self.on_start_pos(piece)
        wall_col = self.any_wall_collisions(piece)
        if wall_col or not on_start:
            return False
        elif self.any_collisions(piece):
            return False
        return True

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
        self._retired_players.add(self._curr_player)
        if self.curr_player % self.num_players != 0:
            self._curr_player = (self._curr_player % self.num_players) + 1
        else:
            self._curr_player = 1

    def get_score(self, player: int) -> int:
        """
        See BlokusBase 
        """
        sum_score = 0
        if len(self.remaining_shapes(player)) == 0:
            if self.player_used_shapes[player][-1] == ShapeKind.ONE:
                return 20
            else:
                return 15
        for each in self.remaining_shapes(player):
            sum_score += len(self._shapes[each].squares)
        return -sum_score

    def available_moves(self) -> set[Piece]:
        """
        See BlokusBase 
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

    def on_start_pos(self, piece:Piece) -> bool:
        """
        Checks of the players piece in the beggining of the game 
        covers one of the designated start position. Additionally, 
        makes sure only one player occupies only 1 starting position. 

        Inputs: 
            piece: Piece 

        Returns, 
            a boolean: True if ONLY ONE square of the layer's peice is 
            on the start position OR if its not the first play made by the player      
        """

        if self.num_moves < self.num_players:
            in_start = 0
            for square in piece.squares():
                if square in self.start_positions:
                    in_start += 1
            if in_start != 1:
                return False
            else:
                return True
        return True
