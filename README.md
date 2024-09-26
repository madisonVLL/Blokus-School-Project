# CMSC 14200 Course Project 

Team members: 
- GUI: Hanim Nuru (hanimn)
- TUI: Madison Vanderbilt (mmv773)
- Bot: Garrett White (garrettwhite)
- QA: Sephora Poteau (poteaus)


## Improvements 

### Game Logic 
[Code Quality]
in BLOKUS.py and PIECE.py, all type annotations were recorded for the 
attributes and variables for the methods. 

[Additional improvement to Game logic]
instead of hard coding the shapes in the previous milestones, 
the from_strings method is used to depeict all the shapes in the game

[Game Logic Completeness]
In PIECE.py, the flip_horizontally method in 
the Shape class is implemented as well as rotations

In BLOKUS.py, the starting_position property now calls for 
the input variable _starting_positions. Before it just output an empty set. 

In the Piece class of the PIECE.py file, intercardinal pieces and 
cardinal pieces method is implemented alot differently and now functionally 
works. 

In BLOKUS.py, the Corners Not Edges rule (using the new implementation of intercardinal 
pieces and cardinal piecies) is implemented in any_collisions,
in which legal to place acknowledges leading to Available moves now working. 

[other comments]
Deleted all the other blokus implementations, 
resulting in the submission of only ONE blokus implementation

[Improvements on functionality] 
In the scenario in which the starting positions are very close together, 
the game logic does not allow the first player to cover more than 1 starting position. 
(implemented in all_starting_pos method). 

Additionally, a new implementation is that when the grid is all filled, 
it will immediately be acknowledged as game over (implemented as a property that is 
called by game_over in the blokus class)


## GUI
[Important notes about the functionality] 
the game will not allow you to choose a piece that will cause a wall collision,
To avoid this, move the pending piece away from the walls to display your current piece. 
Same thing goes for when rotating or flipping. 

When stating your turn, a piece is chosen for the player, but obviously, it is not required
to use that piece during player's turn. 

[Code Quality Comments]
All methods now have docstrings that describe its functionality

[Correctness of GUI Comments]
A player's first piece is randomly selected every time at the 
beginning of the event loop. In addition, player can choose a different shape 
during the event of a key (that represents the shape) being pressing down.

When pressing on (during the Keydown Events inside the event loop) the arrow keys,
e, r and spacebar, piece can now move, rotate or flip horizontally (respectively). 
Additionally, all movement that causes a wall collision is immediately reverted
back to what the piece was before.

When pressing down enter, player can now place a piece
if it follows all the rules of blokus and the game logic (corners not edges, 
and pieces have to start on start_pos for their first turn) 

[Other comment]
GUI can support more than 4 players, but this requires 
having more colors for the player, which I haven't really generalized yet. 

## TUI 
The main feedback that I recieved in Milestone 2 was that a addwstr() error was 
thrown as the terminal size was too small. This ed post discussion discusses 
that the user of the game should change their terminal size manually.

https://edstem.org/us/courses/56801/discussion/4931634

However, between Milestone 2 and 3, I implemented retirements, scores, and ensured
wall collisions were implemented not only in maybe_place and place_piece, but
additionally within simulate_place_piece, which draws a shape on the board before
attempting to place it. 

[Code Quality]
Continued to add doc strings and sufficent variable names 

## Bot
The code saw several revisions to improve readability. Docstrings were 
added to methods to clarify their functionality, making the code easier to 
understand. Type annotations were updated for better compatibility with mypy, 
helping to catch type-related issues early. Additionally, the code was cleaned 
up to meet pylint standards, fixing common issues.

The bot classes were restructured to include a new UBot class, allowing for 
different bot strategies to be tested against each other in Blokus. This 
restructuring made the bot games more flexible and customizable.

The available_moves method was moved to the Blokus class, making it more 
efficient by reducing the number of moves considered because of the corner and 
edge rules. The largest change involved avoiding remaking the board each time 
for availble moves. This change was inspired by suggestions from my post in EDU 
and subsequently the quicker code guide, leading to better performance in move 
generation. Finally, the game over and retiring logic (mostly within the bot file) 
was redone as it was not terminating the game correctly. This was the main issue 
per comments on milestone two. As a result, output was finally achieved, which 
was the major issue in milestone 2. Now the code should run very well!

## QA 


## Enhancements 

Drawn out all the shapes on the display for GUI 
