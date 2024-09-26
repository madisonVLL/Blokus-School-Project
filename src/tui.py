"""
Blokus TUI 
"""

from colorama import Fore, Style

from base import BlokusBase
from fakes import BlokusStub, BlokusFake
from game_types import blockus_games
from piece import Shape, Piece, ShapeKind
from typing import Optional, Any
from blokus import Blokus

import random
import curses
import click

CURRENT_GAME: BlokusBase

#This is the escape key to exit out of tui
ESC = 27

#This is a list of all the enter keys
ENTER_KEYS = [10, 13]

SPACE_BAR = [32, 49, 57]

#These are the arrow keys
ARROW_KEYS = [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]

#These are the key numbers of the number shapes
NUMBER_KEYS: dict[int, str] = {49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 55: "7"}
ROTATION_TYPES: dict[int, str] = {114: "right_rotation", 101: "left_rotation", 32: "space_bar"}

#These are the letter shapes
LETTER_SHAPES: dict[int, str] = {97: "A", 102: "F", 115: "S", 111: "O", 108:"L",
  99: "C", 117: "U", 112: "P", 110: "N", 119: "W", 120: "X", 121: "Y", 122: "Z",
 116: "T", 118: "V"}

#This is the escape key to exit out of tui
ESC = 27

#These are the arrow keys
ARROW_KEYS = [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]

#These key represents q key to retire
QUIT = [113, 81]

#starting the colors for the players and the ga,e
curses.initscr()
curses.start_color()
#colors 1 - 4 represent players
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
#color 5 represents text on screen
curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE)
#this color represents a pending piece
curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_BLACK)
#This color represents the start postions on the board
curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

@click.command()
@click.option('--game', '-g',default="default", help='the game type\
              possible options include: \n\
              mini (1 player\
              mono (1 player)\n \
              duo (2 players) \
              classic (2 - 4 players)')
@click.option('--num_players', '-n', default=2, \
              help='The number of players for each game, between 1 and 4')
@click.option('--start_positions','-p', nargs=2, default=[[4,4],[9,9]], \
multiple=True, help='each start position should be represented as two integers ex x1 y1')
@click.option('--size','-s', default=14, help='size of board, please represented as an int')

def main(game:str, num_players: int, size: int, start_positions: set[tuple[int,int]]) -> None:
    '''
    sets up the blokus game using the click user input parameters
    
    inputs: 
    game: str -> game type represented as a string (classic, mini, duo, default,
    mono)
    num_players: int -> numbers of players represented as a interger
    size: int -> board size of blokus game represented as an int
    start_positions: tuple[tuple[int,int]] -> start positions of pieces 
    represented as a tuple of tuples of ints 
    
    returns:
    None -> creates the blokus game
    '''
    global CURRENT_GAME
    if game != "default":
        if "classic" in game: 
            num_players = int(game[-1])  
            start_positions = blockus_games["classic"]["start_positions"]
            size = blockus_games["classic"]["size"]
        else: 
            game_type = blockus_games[game]
            if game != "mini":
                num_players = game_type["num_players"]
            start_positions = game_type["start_positions"]
            size = game_type["size"]
    
    CURRENT_GAME = Blokus(num_players, size, start_positions)
    curses.wrapper(_main)

def _main(screen) -> None:
   '''
   plays blokus game once the screen is set up
   
   inputs: screen -> instance of curses class
   returns:
   None -> plays blokus game 
    '''
   Blokus_TUI(screen)

class Blokus_TUI:
    board : BlokusBase
    screen : Any
    curr_shape: str
    curr_piece: Piece
    def __init__(self, screen) -> None:
        """
        This function initializes the blokus game class and plays games
        
        Inputs:
        screen: instance of curses board
        
        Returns:
        None
        """
        self.board = CURRENT_GAME
        self.shape_anchor = (self.board.size // 2, self.board.size // 2)
        self.play_blokus(screen)

    def draw_board(self, screen) -> None:
        '''
        this function draws a blokus board utilizing an instance of the Blokus
        game class
        
        inputs:
        self -> instance of BlokusTUI
        screen -> instance of curses class which draws the board on the screen

        returns:
        None -> draws board in place
        '''
        for r in range(self.board.size):
            for c in range(self.board.size):
                if self.board.grid[r][c] != None:
                    player, _ = self.board.grid[r][c]
                    screen.addstr(r + 1, c * 2 + 1, "██", curses.color_pair(player))
                else:
                    screen.addstr(r + 1, c * 2 + 1, "██", curses.color_pair(5))

    def draw_pieces(self, screen) -> None:
        '''
        this function draws a blokus pieces for each player utilizing an 
        instance of the BlokusTUI class
        
        inputs:
        self -> instance of BlokusTUI
        screen -> instance of curses class which draws the board on the screen

        returns:
        None -> draws board in place
        '''
        shape_list: list[str] = [x.value for x in self.board.shapes.keys()]
        
        for player in range(self.board.num_players):
            shape_player = player + 1 
            played_shapes = "Played Shapes: "
            unplayed_shapes = "Unplayed Shapes: "
            for curr_shape in shape_list:
                if curr_shape in [x.value for x in self.board.remaining_shapes(shape_player)]:
                    unplayed_shapes += " " + curr_shape + " │ "
                else:
                    played_shapes += " " + curr_shape + " │ " 
            screen.addstr(self.board.size + 5 + shape_player, 1,\
                           f"Player {shape_player} " + unplayed_shapes + \
                              played_shapes, curses.color_pair(shape_player))
            
    def draw_scores_and_retirements(self, screen) -> None:
        '''
        this function draws the player score and retirements 
        for each player utilizing an instance of the BlokusTUI class
        
        inputs:
        self -> instance of BlokusTUI
        screen -> instance of curses class which scores and retirements
        the board on the screen

        returns:
        None -> draws board in place
        '''
        screen.addstr(1,self.board.size * 2 + 2, f"Player Scores and Retirements")
        for player in range(self.board.num_players):
            screen.addstr(3 + player, self.board.size * 2 + 2, \
            f"Player {player + 1} Score: {self.board.get_score(player + 1)} \
            Retired: {player + 1 in self.board.retired_players}", \
            curses.color_pair(player + 1))

            
    def draw_start_positions(self, screen) -> None:
        '''
        draws start positions on the board
        
        inputs:
        self -> instance of self, particuarly board ans start positions
        screen -> instance of a screen from curses
        
        returns:
        None -> draws start postion on board
        '''
        for point in self.board.start_positions:
            r, c = point
            if self.board.grid[r][c] is None:
                screen.addstr(r + 1, c * 2 + 1, "██", curses.color_pair(7))
            
    def find_shape_from_character(self, screen, shape_char: str) -> None:
        '''
        this function sets the current shape to the keypoard input, prints
        an error message if shape has already been used
        
        inputs:
        self -> instances of BlokusTUI
        screen -> screen to draw on
        shape_char[str] -> keyboard character
        
        returns None 
        -> resets current shape
        '''
        for i, shape_kind in enumerate(self.board.remaining_shapes(self.board.curr_player)):
            if shape_kind.value == shape_char:
                self.curr_shape = shape_kind.value
                self.curr_piece = Piece(self.board.shapes[self.board.\
                                remaining_shapes(self.board.curr_player)[i]])
        if shape_char not in [x.value for x in \
            self.board.remaining_shapes(self.board.curr_player)]:
            screen.addstr(self.board.size + 3,1,\
         f"{shape_char} has already been uses by {self.board.curr_player}\n")

    def stimulate_place_piece(self, screen, anchor_y: int = 1, anchor_x: int = 1) -> None:
        '''
        This function creates a black shape before placing the shape on the board,
        the player can place this shape really anywhere they want to until 
        it become time to place a piece

        inputs:
        self -> instance of self, specifically board, instance of BlokusTUI
        screen -> instance of a screen from curses, screen to draw on
        anchor_y[int] -> integer of row
        anchor_x[int] -> integer of cell

        returns:
        none -> pretends to draw shape on board
        '''
        if self.curr_piece is not None:
            self.curr_piece.set_anchor((anchor_y, anchor_x))
            for each in self.curr_piece.squares():
                r , c = each
                screen.addstr(r + 1, c * 2 + 1, "██", curses.color_pair(6))

    def place_piece(self, screen) -> None:
        '''
        This function determines if a piece can acutally be placed on the blokus 
        board

        self -> instance of BlokusTUI
        screen -> instance of a screen from curses, screen to draw on

        returns:
        none -> places piece on a board if able 
        '''
        if not self.board.maybe_place(self.curr_piece):
            screen.addstr(self.board.size + 5, 1,\
             f"invalid piece position, please attempt \n\
            placing piece in a different position or select a different piece")
        else:
            self.board.maybe_place(self.curr_piece)
            new_shape_index = len(self.board.remaining_shapes(self.board.curr_player)) - 1
            random_piece = random.randint(0, new_shape_index)
            self.curr_piece = Piece(self.board.shapes[self.board.remaining_shapes(self.board.curr_player)[random_piece]])
            self.curr_shape = self.board.remaining_shapes(self.board.curr_player)[random_piece].value
            self.shape_anchor = (self.board.size // 2, self.board.size // 2)

    def valid_piece_relocation(self, point_change: tuple[int, int]) -> bool:
        '''
        determines if a pending piece can be drawn on the board or if there are
        any wall collisions 
        
        inputs:
        self -> instance of BlokusTUI
        point_anchor: tuple[int, int] -> anchor of shape if piece were to move
        
        returns:
        bool -> true is piece can be simulated in the right place, false otherwise
        '''
        r_change, c_change = point_change
        for point in self.curr_piece.squares():
            r, c = point
            if r + r_change not in range(self.board.size) or \
            c + c_change not in range(self.board.size):
                return False
        return True

    def play_blokus(self, screen) -> None:
        '''
        plays blokus game and draws game on board using inputs from keyboard and
        other methods as apart of the BlokusTUI class
        
        inputs:
        self -> instance of BlokusTUI
        screen -> instance of curses

        returns:
        None -> draws board in place
        '''
        self.curr_piece = Piece(self.board.shapes[self.board.remaining_shapes(self.board.curr_player)[5]])
        self.curr_shape = self.board.remaining_shapes(self.board.curr_player)[5].value
        self.curr_piece.set_anchor(self.shape_anchor)
        while True: 
            self.draw_board(screen)
            self.draw_start_positions(screen)
            screen.addstr(self.board.size + 2, 1, \
            f"current player: {self.board.curr_player} \n", curses.color_pair(self.board.curr_player))
            screen.addstr(self.board.size + 3,1, \
            f"current shape: {self.curr_shape} \n", curses.color_pair(self.board.curr_player))

            self.draw_scores_and_retirements(screen)
            self.draw_pieces(screen)

            if self.board.game_over:
                screen.addstr(4 + self.board.num_players, self.board.size * 2 + 2,\
                             f"Congradulations {self.board.winners}! You've won the game!", \
                            curses.color_pair(5))
                screen.addstr(5 + self.board.num_players, self.board.size * 2 + 2,\
                             f"Press ESC to exit the game", \
                            curses.color_pair(5))
                
            #checks to see if shape has already been used or if a shape is none
            if self.curr_shape not in \
                [x.value for x in self.board.remaining_shapes(self.board.curr_player)]\
                      and self.curr_shape is not None:
                    screen.addstr(self.board.size + 4,1,\
                    f"{self.curr_shape} has already been used please select another shape\n")
            if self.curr_shape is None:
                screen.addstr(self.board.size + 4,1, f"please select a shape\n")


            self.stimulate_place_piece(screen, self.shape_anchor[0], self.shape_anchor[1])

            curr_character =  screen.getch()

            if curr_character == ESC:
                break
            if self.curr_piece is not None:

                #if the current character is equal to space
                if curr_character in SPACE_BAR:
                    screen.addstr(self.board.size + 2, 1, f" pressed space bar \n")


                if curr_character == ARROW_KEYS[0]:
                    #this would be the left key
                    if self.valid_piece_relocation((0, - 1)):
                        self.shape_anchor = (self.shape_anchor[0], self.shape_anchor[1] - 1)

                if curr_character == ARROW_KEYS[1]:
                    #this would be the right key
                    if self.valid_piece_relocation((0,1)):
                        self.shape_anchor = (self.shape_anchor[0], self.shape_anchor[1] + 1)

                if curr_character == ARROW_KEYS[2]:
                    #this would be the up key
                    if self.valid_piece_relocation((-1, 0)):
                        self.shape_anchor = (self.shape_anchor[0] - 1, self.shape_anchor[1])

                if curr_character == ARROW_KEYS[3]:
                    #this would be the down key
                    if self.valid_piece_relocation((1, 0)):
                        self.shape_anchor = (self.shape_anchor[0] + 1, self.shape_anchor[1])


                if curr_character in ENTER_KEYS:
                    self.place_piece(screen)
            
            if curr_character in NUMBER_KEYS:
                curr_shape_str = NUMBER_KEYS[curr_character]
                self.curr_shape = NUMBER_KEYS[curr_character]
                if curr_shape_str not in [x.value for x in self.board.remaining_shapes(self.board.curr_player)]:
                    screen.addstr(self.board.size + 4,1, f"current shape: {self.curr_shape}  has already been uses\n")
                for shape in self.board.remaining_shapes(self.board.curr_player):
                    if shape.value == curr_shape_str:
                        self.curr_shape = curr_shape_str
                        self.curr_piece = Piece(self.board.shapes[shape])
                        self.curr_piece.set_anchor((self.board.size // 2, self.board.size // 2))

            if curr_character in LETTER_SHAPES:
                self.curr_shape = LETTER_SHAPES[curr_character]
                if LETTER_SHAPES[curr_character] not in [x.value for x in self.board.remaining_shapes(self.board.curr_player)]:
                    screen.addstr(self.board.size + 3,1, f"current shape: {self.curr_shape}  has already been uses\n")
                for shape in self.board.remaining_shapes(self.board.curr_player):
                    if shape.value == LETTER_SHAPES[curr_character]:
                        self.curr_shape = LETTER_SHAPES[curr_character]
                        self.curr_piece = Piece(self.board.shapes[shape])
                        self.curr_piece.set_anchor((self.board.size // 2 + 1, self.board.size // 2 + 1))
                
            if curr_character in ROTATION_TYPES:
                if self.curr_piece is not None: 
                    if ROTATION_TYPES[curr_character] == "space_bar":
                        self.curr_piece.flip_horizontally()
                    if ROTATION_TYPES[curr_character] == "left_rotation":
                        self.curr_piece.rotate_left()
                    if ROTATION_TYPES[curr_character] == "right_rotation":
                        self.curr_piece.rotate_right()

            if curr_character in QUIT:
                screen.addstr(self.board.size + 5,1, f"Player {self.board.curr_player} has retired\n")
                self.board.retire()
                    
            screen.clear()
            screen.refresh()

if __name__ == "__main__":
    main()