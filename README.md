# CMSC 14200 Course Project - Blokus Game
## TUI: Madison Vanderbilt (mmv773)

### How To Run TUI
1. Clone GitHub Respiratory
2. Ensure that terminal if full size of your window, otherwise game won't run
3. Enter src folder
4. in command line, run *python3 tui.py*
This game supports 2 - 4 players and a default board size of 14 and default start positions at (4, 4) and (9, 9). You have the opportunity to change this by the following command line inputs:
-n NUM_PLAYERS / --num-players NUM_PLAYERS to specify the number of players. The default is 2.

** example **
*python3 tui.py -n 3* (specify three players)

-s BOARD_SIZE / --size BOARD_SIZE to specify the board size. The default is 14.

** example **
*python3 tui.py -s 20* (specify 20 x 20 board)

** example **

-p X Y / --start-position X Y to define a start position. Multiple start positions should be possible by writing, for example, -p X1 Y1 -p X2 Y2 -p X3 Y3.

*python3 tui.py -p 3 3 -p 5 5 -p 9 9* (starting positions at (3, 3), (5, 5), (9, 9))

** example **

-game GAMETYPE

*python3 tui.py --game=mono* specify the Blokus Mono configuration (one player on a smaller board)

*python3 tui.py--game=duo* to specify the Blokus Duo configuration specify the Blokus Mono configuration (two player on a smaller board)

*python3 tui.py --game=classic-2, --game=classic-3*, and *--game=classic-4* to specify Blokus Classic with 2, 3, or 4 players, respectively.


