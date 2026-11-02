import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from game import TicTacToe, get_winner, best_move

def test_winner_detection():
    assert get_winner(("X", "X", "X", "", "", "", "", "", "")) == "X"
    assert get_winner(("O", "", "", "O", "", "", "O", "", "")) == "O"
    assert get_winner(("", "", "", "", "", "", "", "", "")) is None

def test_ai_returns_valid_empty_square():
    board = ("X", "", "", "", "O", "", "", "", "X")
    move = best_move(board)
    assert move is not None
    assert board[move] == ""

def test_game_rejects_occupied_square():
    game = TicTacToe()
    assert game.play(0) is True
    assert game.play(0) is False

def test_new_round_keeps_score():
    game = TicTacToe()
    game.score["X"] = 2
    game.new_round()
    assert game.score["X"] == 2
    assert game.moves == 0
