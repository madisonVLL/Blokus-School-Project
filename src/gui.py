import sys
import os 
from piece import Point, Shape, Piece
import click
import random 

from typing import Callable
from game_types import blockus_games
from blokus import Blokus


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.gfxdraw

PLAYER_COLORS = [(250,100,100), (34,139,34), (100,100,250), (221,160,221), (250,250,102)]
PLAYER_DISPLAY = [(250,180,190), (1,50,32), (173,216,230), (75,0,130),(204,204,0)]
#only 4 colors, which means it only supports 4 players, however, if colors
# are generalized, then can support up to any number of players. 

flo_Point = tuple[float,float]
flo_Rect = tuple[flo_Point,flo_Point]


def center_of_tup(ls: list[tuple[int,int]]) -> tuple[int,int]:
    xis = []
    yis = []
    mean: Callable = lambda x: sum(x)//len(x)
    for tup in ls: 
        yis.append(tup[0])
        xis.append(tup[1])
    return (mean(xis),mean(yis))

class Blokus_gui:
    
    font: pygame.font.Font

    def __init__(self, grid_size:int,
                  num_players:int, start_pos: set[Point]) -> None:
        
        self.official_size: int = 600
        self.num_players: int = num_players 
        self.grid_size: int = grid_size 
        self.start_pos: set[Point]= start_pos
        
        
        self.box_size: float = self.official_size//self.grid_size 
        self.spacer: float = self.box_size/10
        self.wid_hei:float = self.box_size*(self.grid_size) + self.spacer*(self.grid_size) 

        self.box: flo_Rect = ((self.spacer,self.spacer), (self.wid_hei,self.wid_hei))
        self.box_dim: Point = (self.box_size,self.box_size)
        # sizes for boxes and grid

        self.col_row: list[float]= []
        for col_row in list(range(self.grid_size)):
            self.col_row.append(
                self.spacer + self.spacer*col_row + self.box_size*col_row)
      
        self.box_grid: list[list[flo_Point]] = []
        for row in self.col_row: 
            colum = []
            for col in self.col_row: 
                colum.append((row,col))
            self.box_grid.append(colum)
        # sets up the grid

        self.op_grid:Callable = lambda x: self.box_size*(x) + self.spacer*(x+1) 
        # function adjusts Points for display

        self.rect_for_pieces: flo_Rect = ((float(0),self.wid_hei), 
                                            (self.wid_hei,self.wid_hei//1.75))
        self.game_shapes:float = self.official_size//45
        self.op2:Callable = lambda x1: (x1)*self.game_shapes + 10 
        # for displaying the player's peices
    
        self.player_col: dict[int,tuple[int,int,int]] = dict()
        self.player_display: dict[int,tuple[int,int,int]] = dict()
        for i in range(self.num_players):
            self.player_col[i+1] = PLAYER_COLORS[i]
            self.player_display[i+1] = PLAYER_DISPLAY[i]
         # distinguishing players by color 

        self.track_game: flo_Rect = ((float(0),self.wid_hei*1.37),
                                        (self.wid_hei,self.wid_hei))

        self.surface_area: flo_Point = (self.wid_hei,self.wid_hei*1.50)
        self.middle = (self.wid_hei//4, self.wid_hei//2)
        self.font_size: int = self.game_shapes*2
        #size variables used throughout
        
        self.surface = pygame.display.set_mode(self.surface_area)
        self.game: Blokus = Blokus(self.num_players, self.grid_size, 
                    self.start_pos)
        
        pygame.init()
        pygame.display.set_caption("Blokus")  
        self.font = pygame.font.Font(None,self.font_size)                                                      
        self.event_loop()                       

                       
    def draw_box(self, rect: flo_Point, start:bool = False,
                 color:tuple[int,int,int] = (215,245,245)) -> None:  
        """
        Draws the boxes on the grid. If the box on a grid represents a start
        position, it will draw it to be black

        Inputs: 
            rect, a tuple of ints 
            start, a bool 
            color, tuple of ints represents the RGB 
        """
        if start: 
            color = (0,0,0)
    
        pygame.draw.rect(self.surface, color, (rect,(self.box_dim)))
                                            
    def _shapes_to_place(self, index: int, shape_points: Point, 
                         for_text: bool = False) -> Point:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        """
        Given points of a shape, it uses the index of a loop to draw pieces for the player. 
        Additionally, it's used to display text to describe the shape to the player. 
        Function returns specific position on the display. 

        Inputs: 
            index, an int
            shape_points, a Point 
            for_text, a default boolean
        
        Returns, a Point 
        """    
        r,c = shape_points 
        away = 0 
        if for_text: 
            away = 40
        if index > 10: 
            index = 21-index
            row = 1.25 
        else: 
            row = 1.05

        height = self.op2(r) + self.wid_hei *row + away 
        left = self.op2(c) + (self.wid_hei//11)* index
        
        return (height,left)
    
    def display_player_score(self) -> None:
        """
        At the bottom of the screen it displays the players
        and their score
        """
        self.surface.fill((255,255,255), rect= self.track_game)
        right, _ = self.track_game 

        width = right[1]
        if self.game.num_players == 1: 
            adjust =  self.wid_hei//1.15
        else: 
            adjust = right[1]//(self.game.num_players*2)
        
        size_for_player = width//self.game.num_players - adjust 


        for i in range(self.num_players): 
            if (i+1) in self.game.retired_players:
                col = (128,128,128)
            
            if (i+1) in self.game.winners or not (i+1) in self.game.retired_players: 
                col = self.player_col[i+1]

            text_name = self.font.render(f"player {i+1}",True,col)
            text_score = self.font.render(f"{self.game.get_score(i+1)}", True, col)
            
            self.surface.blit(text_name,(size_for_player+ (i*adjust),right[1]+20))
            self.surface.blit(text_score,(size_for_player+ (i*adjust), right[1]+40))

        
    def curr_player_pieces(self) -> None:
        """
        Displays the shape and the type of shape in text of the 
        current player's peices. 
        """
        curr_player = self.game.curr_player
        display_col = self.player_display[curr_player]

        self.surface.fill(display_col, rect= self.rect_for_pieces)

        for enum_i, ls_shapes in enumerate(self.game.shapes):

            squares = self.game.player_shapes_dict[curr_player][ls_shapes]
            remaining = self.game.remaining_shapes(curr_player)
            
            for_text = []
            for shape_points in squares.squares:
                
                r,c = shape_points
                height,left = self._shapes_to_place(enum_i, (r,c))
                
                for_text.append(self._shapes_to_place(enum_i, (r,c),True))                
                if squares.kind not in remaining: 
                    col = (128,128,128)
                else: 
                    col = self.player_col[self.game.curr_player]

                value = self.game_shapes
                self.surface.fill(color = col,rect=((left,height),(value,value)))
            
            center = center_of_tup(for_text)
            col = self.player_col[self.game.curr_player]
            text = self.font.render(ls_shapes.value,True,col)
            self.surface.blit(text, center)
    
    def pending_piece(self, shape:Shape, r_anchor: int, c_anchor: int) -> Piece: 
        """
        Given a shape and its anchor points, it will return piece and displays the piece
        in a Blue color, which is distinct from the player's pieces 

        Inputs: 
            shape, a Shape 
            r_anchor, an int 
            c_anchor, an int 
        
        Returns, a Piece 
        """
     
        shape_piece = Piece(shape)
        shape_piece.set_anchor((r_anchor,c_anchor))

        for points in shape.squares:
            r,c = points 
            rect = (self.op_grid(c+shape_piece.anchor[1]),
                    self.op_grid(r+shape_piece.anchor[0]))
            self.draw_box(rect,color=(0,0,139))

        return shape_piece
    

    def display_starting(self) -> None:
        """
        Displays all the starting postions on the board 
        """  
        for start in self.start_pos:       
            r,c = start 
            if self.game.grid[r][c] == None: 
                self.draw_box((self.op_grid(c),self.op_grid(r)),start=True) 

    def draw_grid(self) -> None:
        """
        Draws the entire grid given its grid_size

        If a player's peice was placed on the position, it will change to the player's 
        piece permanentely. If no piece is "hovering" or placed in that position, square
        on grid is set to the origin white color.
        """
        self.surface.fill((250,250,250))
        pygame.draw.rect(self.surface,(250,250,250),
                         rect = ((0,0),(self.wid_hei,self.wid_hei)), width = 4)
        
        for col_num, col in enumerate(self.box_grid):
            for row_num, row in enumerate(col):
                tup_of_grid = self.game.grid[row_num][col_num]
                if tup_of_grid != None: 
                    player,_ = tup_of_grid
                    self.draw_box((row), color= self.player_col[player])
                else: 
                    self.draw_box((row))   
    
    
    def check_walls(self,shape:Shape, 
                           r_anchor: int, c_anchor: int) -> bool:
        """
        Checks if a given shape has collided with the wall. Used when rotating, flipping or 
        choosing a piece. If there is a wall collision it will return True
        
        Input: 
            shape, A Shape
            r_anchor, an int 
            c_anchor, an int 
        
        Returns, a boolean
        """
        piece = Piece(shape)
        piece.set_anchor((r_anchor, c_anchor))
        return self.game.any_wall_collisions(piece)
    
    def game_is_over(self) -> None:
        """
        Displays the Screen for when the game is over  
        """
        if self.game.game_over:
                self.surface.fill((0,0,0))
                str_winner = ', '.join([str(x) for x in self.game.winners])
                if len(self.game.winners) > 1: 
                    col = (250,250,250)                       
                    text = self.font.render(f"THE BLOKUS WINNERS ARE PLAYERS {str_winner}",True,col)
                else: 
                    col = self.player_col[int(str_winner)]
                    text = self.font.render(f"THE BLOKUS WINNER IS PLAYER {str_winner}",True,col)

                self.display_player_score()
                self.surface.blit(text,self.middle)
    
    def event_loop(self) -> None:
        """git 
        Game event as defined by the blokus specifications
        """
        chosen = random.choice(self.game.remaining_shapes(self.game.curr_player)) 
        this_shape = self.game.player_shapes_dict[self.game.curr_player][chosen]
        r_anchor, c_anchor = (self.grid_size//2,self.grid_size//2) 
        
        while True:   
            events = pygame.event.get()
            self.draw_grid()
            self.curr_player_pieces()
            self.display_starting()
            self.display_player_score()
            this_piece = self.pending_piece(this_shape, r_anchor,c_anchor)
            self.game_is_over()
  
            for event in events: 
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN 
                                                 and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    new = str(event.dict["unicode"]).upper()
                    for kind in self.game.remaining_shapes(self.game.curr_player):
                        if new == kind.value:
                            new_shape = self.game.player_shapes_dict[self.game.curr_player][kind]
                            if not self.check_walls(new_shape,r_anchor,c_anchor):
                                this_shape = new_shape
                  
                    if event.key == pygame.K_UP: 
                        if not self.check_walls(this_shape,r_anchor-1,c_anchor):               
                            r_anchor += -1 

                    if event.key == pygame.K_DOWN:
                        if not self.check_walls(this_shape,r_anchor+1,c_anchor):               
                            r_anchor += 1 
    
                    if event.key == pygame.K_LEFT:
                        if not self.check_walls(this_shape,r_anchor,c_anchor-1):               
                            c_anchor += -1 
            
                    if event.key == pygame.K_RIGHT:
                        if not self.check_walls(this_shape,r_anchor,c_anchor+1):               
                            c_anchor += 1 

                    if event.key == pygame.K_r:
                        this_shape.rotate_right()
                        if self.check_walls(this_shape,r_anchor,c_anchor):
                            this_shape.rotate_left()

                    if event.key == pygame.K_e:
                        this_shape.rotate_left() 
                        if self.check_walls(this_shape,r_anchor,c_anchor):
                            this_shape.rotate_right()

                    if event.key == pygame.K_SPACE:
                        this_shape.flip_horizontally() 
                        if self.check_walls(this_shape,r_anchor,c_anchor):
                            this_shape.flip_horizontally()

                    if event.key == pygame.K_6:
                        if self.game.maybe_place(this_piece): 
                            if self.game.game_over: 
                                self.game_is_over
                            else: 
                                self.event_loop()
                    
                    if event.key == pygame.K_q:
                        self.game.retire()

            pygame.display.update()


choice_for_classic = [f"classic-{i}" for i in range(1,20)] 
# technically classic has a limit to 19 number of players

all_choices = ["mono","duo"] + choice_for_classic

@click.command("blokus-gui")
@click.option('--num_players', '-n', type=click.INT, default=2,
               help="Setting the number of Players for blokus game")
@click.option("-s", "--size", type=click.INT, default = 14,
               help="Setting the size of the board")
@click.option("-p", "--start_position", nargs=2, multiple=True, default = [(4,4),(9,9)],
               help="The starting position for players")   

@click.option("--game", type=click.Choice(all_choices), 
              help="Setting the game type")

def blokus_cmd(game:str, num_players: int, size: int,
                start_position: set[tuple[int,int]]) -> None:
    """
    Uses Command line parameters to set the board for Blokus
    
    Inputs: 
        game, a str
        num_players, an int
        size, an int
        start_position, a tuple of Points
    """
    if game != None:
        if "classic" in game: 
            types = blockus_games["classic"]
            players = int(game[-1])       
        else: 
            types = blockus_games[game]
            players=types["num_players"]
        
        Blokus_gui(grid_size=types["size"],
                num_players=players,start_pos=types["start_positions"])
    
    Blokus_gui(size,num_players,start_position)

if __name__ == "__main__":
   blokus_cmd()
