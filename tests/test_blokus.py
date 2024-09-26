"""
CMSC 14200 Blokus Proj.
Dear God I'm so tired :(
"""

def test_inheritance(self):
    """
    Test that Blokus Inherits from BlokusBase
    """
    raise NotImplementedError
    
def test_init_blokus_mini_1(self):
    """
    Construct an instance of a 1-player Blokus Mini game configuration.
    Verify that the size, start_positions, num_players, and curr_player
    properties have been initialized correctly. Also verify that grid has
    been initialized correctly.
    """
    raise NotImplementedError
    
def test_init_blokus_mini_2(self):
    """
    Construct an instance of a 2-player Blokus Mini game configuration.
    Verify that the size, start_positions, num_players, and curr_player
    properties have been initialized correctly. Also verify that grid has
    been initialized correctly.
    """
    raise NotImplementedError

def test_init_blokus_mono(self):
    """
    Construct an instance of a Blokus-Mono Blokus Mini game configuration.
    Verify that the size, start_positions, num_players, and curr_player
    properties have been initialized correctly. Also verify that grid has
    been initialized correctly.
    """
    raise NotImplementedError

def test_init_blokus_duo_2(self):
    """
    Construct an instance of a Blokus-Duo Blokus Mini game configuration.
    Verify that the size, start_positions, num_players, and curr_player
    properties have been initialized correctly. Also verify that grid has
    been initialized correctly.
    """
    raise NotImplementedError

def test_shapes_loaded(self):
    """
    Construct an instance of any Blokus game configuration, and test that
    the shapes dictionary has been correctly initialized with all 21 Blokus
    shapes. (Notice that test_some_shapes_loaded provided in tests/test_fake.py
    checks only that some shapes have been loaded correctly.)
    """
    raise NotImplementedError

def test_some_flipped_shapes(self):
    """
    Construct an instance of any Blokus game configuration, and test that at
    least three kinds of shapes can be flipped correctly via the
    Shape.flip_horizontally method.
    """
    raise NotImplementedError

def test_some_left_rotated_shapes(self):
    """
    Construct an instance of any Blokus game configuration, and test that at
    least three kinds of shapes can be flipped correctly via the
    Shape.rotate_left method.
    """
    raise NotImplementedError

def test_some_right_rotated_shapes(self):
    """
    Construct an instance of any Blokus game configuration, and test that at
    least three kinds of shapes can be flipped correctly via the
    Shape.rotate_right method.
    """
    raise NotImplementedError

def test_some_cardinal_neighbors(self):
    """
    Construct an instance of any Blokus game configuration, and test that
    Piece.cardinal_neighbors correctly computes the cardinal neighbors of at
    least three kinds of pieces. For the purposes of this test, the pieces can
    remain in their 'initial' orientation, before being subjected to any flips
    or rotations.
    """
    raise NotImplementedError

def test_some_intercardinal_neighbors(self):
    """
    Construct an instance of any Blokus game configuration, and test that
    Piece.intercardinal_neighbors correctly computes the cardinal neighbors of at
    least three kinds of pieces. For the purposes of this test, the pieces can
    remain in their 'initial' orientation, before being subjected to any flips
    or rotations.
    """
    raise NotImplementedError

def test_one_player_blokus_mini_game(self):
    """
    Construct a 1-player Blokus mini game configuration. Test that the player can
    place two or more pieces before retiring. At each step before game over, verify
    that the values of game_over and curr_player are correct. After game over, verify
    the values of game_over, winners, and get_score(1).
    """
    raise NotImplementedError

def test_two_player_blokus_mini_game(self):
    """
    Construct a 2-player Blokus mini game configuration. Test that each player can place
    two or more pieces before retiring. At each step before game over, verify that the
    values of game_over and curr_player are correct. After game over, verify the values
    of game_over, winners, get_score(1), and get_score(2).
    """
    raise NotImplementedError