# CMSC 14200 Course Project - Blokus Game
## Contribution: TUI and Game Logic
For this project, I was in charge of creating the Text User Interface (TUI) version of this Blokus game. Additionally, I built features of the game logic for all game versions including the GUI and Bot. These features include: adding piece to board, ensuring valid piece placement, determining intercardinal squares on the board, and creating game pieces. 

### About Blokus
[**Blokus**]([https://en.wikipedia.org/wiki/Blokus]))*(/ˈblɒkəs/ BLOK-əs)* is an abstract strategy board game for two to four players, where players try to score points by occupying most of the board with pieces of their colour.

How To Play: [Play Blokus](https://service.mattel.com/instruction_sheets/BJV44-Eng.pdf)

### How To Run TUI
1. Clone GitHub Respiratory
2. Ensure that terminal if full size of your window, otherwise game won't run
3. Enter src folder
4. in command line, run *python3 tui.py* 


This game supports 2 - 4 players and a default board size of 14 and default start positions at (4, 4) and (9, 9). You have the opportunity to change this by the following command line inputs:
-n NUM_PLAYERS / --num-players NUM_PLAYERS to specify the number of players. The default is 2.

**example** *python3 tui.py -n 3* (specify three players)

-s BOARD_SIZE / --size BOARD_SIZE to specify the board size. The default is 14.

**example** *python3 tui.py -s 20* (specify 20 x 20 board)

-p X Y / --start-position X Y to define a start position. Multiple start positions should be possible by writing, for example, -p X1 Y1 -p X2 Y2 -p X3 Y3.

**example** *python3 tui.py -p 3 3 -p 5 5 -p 9 9* (starting positions at (3, 3), (5, 5), (9, 9))

-game GAMETYPE

**example** 
*python3 tui.py --game=mono* specify the Blokus Mono configuration (one player on a smaller board)

*python3 tui.py--game=duo* to specify the Blokus Duo configuration specify the Blokus Mono configuration (two player on a smaller board)

*python3 tui.py --game=classic-2, --game=classic-3*, and *--game=classic-4* to specify Blokus Classic with 2, 3, or 4 players, respectively.


