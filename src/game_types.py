"""
Dictionary which stores some information storing different game types
"""

blockus_games: dict[str, dict[str, set[tuple[int,int]]|int]] = {
    "duo": {"size": 14, "num_players": 2, "start_positions": {(4, 4), (9,9)}} ,
    "mini":  {"size": 5,  "start_positions":{(0, 0), (4, 4)}},
    "mono": {"size": 11, "num_players": 1,  "start_positions": {(5, 5)}},
    "classic": {"size": 20, "start_positions": {(0, 0), (19, 19), (0, 19), (19, 0)}},
}