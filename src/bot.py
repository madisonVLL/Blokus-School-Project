"""
Blokus Bot File

This module contains classes for different bots for playing Blokus
"""

from abc import ABC, abstractmethod
import random
import click
from blokus import Blokus
from piece import Piece

class BaseBot(ABC):
    """
    Represents a base bot playing Blokus
    """

    def __init__(self, bot_id: int):
        self.bot_id = bot_id

    @abstractmethod
    def make_move(self, game: Blokus) -> Piece | None:
        """
        Make move
        """

    def play_game(self, opponent: 'BaseBot', num_games: int) -> tuple[int, int, int]:
        """
        Blokus with specific bots and return the results

        Inputs:
            opponent (BaseBot): The opponent bot
            num_games (int): The number of games to play

        Returns:
            tuple[int, int, int]: A tuple containing the 
            number of wins for self, opponent, and ties
        """

        ties = 0
        self_wins = 0
        opponent_wins = 0

        for _ in range(num_games):
            game = Blokus(num_player=2, size=11, start_positions={(0, 0), (10, 10)})
            current_bot = self
            game_over = False

            while not game_over:
                move = current_bot.make_move(game)
                if move:
                    game.maybe_place(move)
                else:
                    game.retire()

                current_bot = opponent if current_bot == self else self
                game_over = game.game_over

            winners = game.winners
            if len(winners) == 2:
                ties += 1
            elif self.bot_id in winners:
                self_wins += 1
            else:
                opponent_wins += 1

        return self_wins, opponent_wins, ties

class NBot(BaseBot):
    """
    Represents a random-playing bot (needs improvement) in Blokus
    """

    def make_move(self, game: Blokus) -> Piece | None:
        available_moves = game.available_moves()
        if available_moves:
            return random.choice(list(available_moves))
        return None

class SBot(BaseBot):
    """
    Represents a smart bot in Blokus
    """

    def make_move(self, game: Blokus) -> Piece | None:
        available_moves = list(game.available_moves())
        if available_moves:
            random_moves = random.sample(available_moves, min(20, len(available_moves)))
            best_move = self.evaluate_moves(random_moves)
            return best_move
        return None

    def evaluate_moves(self, random_moves: list[Piece]) -> Piece | None:
        """
        Evaluates the available moves and returns the best move

        Inputs:
            random_moves (list[Piece]): The list of available moves.
            game (Blokus): The Blokus game instance

        Returns:
            Piece: The best move to be placed on the board
        """

        best_move = None
        best_score = 0

        for move in random_moves:
            score = self.evaluate_move(move)
            if score > best_score:
                best_move = move
                best_score = score

        return best_move

    def evaluate_move(self, move: Piece) -> int:
        """
        Evaluate the move based on its score by length

        Inputs:
            move (Piece): The move to be evaluated
            game (Blokus): The Blokus game instance

        Returns:
            int: The score of the move
        """

        return len(move.squares())

class UBot(BaseBot):
    """
    Represents an unsatisfactory bot (worse than random) in Blokus
    """

    def make_move(self, game: Blokus) -> Piece | None:
        available_moves = list(game.available_moves())
        if available_moves:
            random_moves = random.sample(available_moves, min(20, len(available_moves)))
            worst_move = self.evaluate_moves(random_moves)
            return worst_move
        return None

    def evaluate_moves(self, random_moves: list[Piece]) -> Piece | None:
        """
        Evaluates the available moves and returns the worst move

        Inputs:
            random_moves (list[Piece]): The list of available moves
            game (Blokus): The Blokus game instance

        Returns:
            Piece: The best move to be placed on the board
        """

        worst_move = None
        worst_score = float('inf')

        for move in random_moves:
            score = self.evaluate_move(move)
            if score < worst_score:
                worst_move = move
                worst_score = score

        return worst_move

    def evaluate_move(self, move: Piece) -> float:
        """
        Evaluate the move based on its score by length

        Inputs:
            move (Piece): The move to be evaluated
            game (Blokus): The Blokus game instance

        Returns:
            int: The score of the move
        """

        return len(move.squares())

@click.command()
@click.option('-n', '--num-games', default=20, type=int, \
help='Number of games to play.')
@click.option('-1', '--player1', default='N', \
type=click.Choice(['S', 'N', 'U']), help='Strategy for player 1.')
@click.option('-2', '--player2', default='N', \
type=click.Choice(['S', 'N', 'U']), help='Strategy for player 2.')

def main(num_games: int, player1: str, player2: str) -> str:
    """
    Run to play Blokus games with specified strategies

    Inputs:
        num_games (int): Number of games to play
        player1 (str): Strategy for player 1
        player2 (str): Strategy for player 2
    """

    strategies = {'N': NBot, 'S': SBot, 'U': UBot}

    bot1 = strategies[player1](bot_id=1)
    bot2 = strategies[player2](bot_id=2)

    bot1_wins, bot2_wins, ties = bot1.play_game(bot2, num_games)

    total_games = num_games
    ties_percentage = (ties / total_games) * 100
    bot1_win_percentage = (bot1_wins / total_games) * 100
    bot2_win_percentage = (bot2_wins / total_games) * 100

    print(f"Bot 1 ({player1}) Wins | {bot1_win_percentage:.2f} %")
    print(f"Bot 2 ({player2}) Wins | {bot2_win_percentage:.2f} %")
    print(f"Ties           | {ties_percentage:.2f} %")

if __name__ == "__main__":
    main()
