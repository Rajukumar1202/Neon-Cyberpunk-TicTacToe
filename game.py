
import random
import json
import os
from functools import lru_cache


# ==================================================
# CONSTANTS
# ==================================================

WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
)

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "player_data.json"
)

ACHIEVEMENTS = {
    "First Victory": {
        "description": "Win your first match",
        "target": 1
    },
    "Five Wins": {
        "description": "Win 5 matches",
        "target": 5
    },
    "Winning Streak": {
        "description": "Win 3 matches in a row",
        "target": 3
    },
    "AI Destroyer": {
        "description": "Win 5 matches against AI",
        "target": 5
    },
    "Perfect Player": {
        "description": "Win 10 matches",
        "target": 10
    }
}


# ==================================================
# BASIC GAME FUNCTIONS
# ==================================================

def get_winner(board):
    """Check whether X or O has won."""

    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    return None


def empty_cells(board):
    """Return all empty board positions."""

    return [
        i for i, cell in enumerate(board)
        if not cell
    ]


# ==================================================
# MINIMAX AI
# ==================================================

@lru_cache(maxsize=None)
def minimax(board, player):
    """Calculate the best possible outcome for Hard AI."""

    winner = get_winner(board)

    if winner == "O":
        return 10

    if winner == "X":
        return -10

    if not any(not cell for cell in board):
        return 0

    scores = []

    for i in empty_cells(board):

        next_board = list(board)
        next_board[i] = player

        next_player = "X" if player == "O" else "O"

        scores.append(
            minimax(tuple(next_board), next_player)
        )

    return max(scores) if player == "O" else min(scores)


def best_move(board):
    """Find optimal move for Hard AI."""

    best_score = float("-inf")
    moves = []

    for i in empty_cells(board):

        candidate = list(board)
        candidate[i] = "O"

        score = minimax(tuple(candidate), "X")

        if score > best_score:
            best_score = score
            moves = [i]

        elif score == best_score:
            moves.append(i)

    return random.choice(moves) if moves else None


def medium_move(board):
    """Win, block, prefer center, otherwise choose randomly."""

    # Try to win
    for i in empty_cells(board):

        candidate = list(board)
        candidate[i] = "O"

        if get_winner(tuple(candidate)) == "O":
            return i

    # Block X
    for i in empty_cells(board):

        candidate = list(board)
        candidate[i] = "X"

        if get_winner(tuple(candidate)) == "X":
            return i

    # Prefer center
    if 4 in empty_cells(board):
        return 4

    return random.choice(empty_cells(board))


# ==================================================
# MAIN GAME CLASS
# ==================================================

class TicTacToe:
    """Tic-Tac-Toe with AI, achievements, replay and tournaments."""

    def __init__(self):

        self.mode = "AI"
        self.difficulty = "Hard"
        self.sound_on = True

        self.score = {
            "X": 0,
            "O": 0,
            "Draw": 0
        }

        # Persistent player data
        self.player_data = self.load_player_data()

        # Replay data
        self.replay_moves = []
        self.last_replay = None
        self.replay_board = [""] * 9
        self.replay_index = 0
        self.replay_active = False

        # AI personality
        self.ai_message = "Let's play! I am ready."

        # Tournament
        self.tournament = {
            "active": False,
            "best_of": 3,
            "wins": {"X": 0, "O": 0},
            "draws": 0,
            "rounds": 0,
            "champion": None
        }

        self.reset_board()

    # ==================================================
    # PERSISTENT DATA
    # ==================================================

    def default_player_data(self):

        return {
            "total_matches": 0,
            "wins_X": 0,
            "wins_O": 0,
            "draws": 0,
            "ai_wins": 0,
            "total_wins": 0,
            "current_streak": 0,
            "best_streak": 0,
            "last_winner": None,
            "unlocked": [],
            "match_history": []
        }

    def load_player_data(self):
        """Load saved statistics from JSON."""

        defaults = self.default_player_data()

        try:
            if os.path.exists(DATA_FILE):

                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    saved = json.load(file)

                if isinstance(saved, dict):
                    defaults.update(saved)

        except (OSError, json.JSONDecodeError):
            pass

        return defaults

    def save_player_data(self):
        """Save achievements and statistics."""

        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    self.player_data,
                    file,
                    indent=4
                )

        except OSError:
            print("Warning: Could not save player data.")

    # ==================================================
    # ACHIEVEMENT SYSTEM
    # ==================================================

    def unlock_achievement(self, name):
        """Unlock achievement if it is not already unlocked."""

        if name not in self.player_data["unlocked"]:

            self.player_data["unlocked"].append(name)

            self.ai_message = (
                f"Achievement unlocked: {name}!"
            )

            self.save_player_data()

            return True

        return False

    def update_achievements(self, winner):

        data = self.player_data

        if winner not in ("X", "O"):
            return

        if data["total_wins"] >= 1:
            self.unlock_achievement("First Victory")

        if data["total_wins"] >= 5:
            self.unlock_achievement("Five Wins")

        if data["current_streak"] >= 3:
            self.unlock_achievement("Winning Streak")

        if data["ai_wins"] >= 5:
            self.unlock_achievement("AI Destroyer")

        if data["total_wins"] >= 10:
            self.unlock_achievement("Perfect Player")

    def get_achievements(self):
        """Return achievement details and unlock status."""

        unlocked = self.player_data["unlocked"]

        result = []

        for name, details in ACHIEVEMENTS.items():

            result.append({
                "name": name,
                "description": details["description"],
                "unlocked": name in unlocked
            })

        return result

    # ==================================================
    # MATCH STATISTICS
    # ==================================================

    def update_statistics(self, winner):

        data = self.player_data

        data["total_matches"] += 1

        if winner == "Draw":

            data["draws"] += 1
            data["current_streak"] = 0
            data["last_winner"] = None

        else:

            data[f"wins_{winner}"] += 1
            data["total_wins"] += 1

            if self.mode == "AI" and winner == "X":
                data["ai_wins"] += 1

            if data["last_winner"] == winner:
                data["current_streak"] += 1
            else:
                data["current_streak"] = 1

            data["last_winner"] = winner

            data["best_streak"] = max(
                data["best_streak"],
                data["current_streak"]
            )

            self.update_achievements(winner)

        data["match_history"].append({
            "winner": winner,
            "mode": self.mode,
            "difficulty": self.difficulty
        })

        # Keep only latest 50 records
        data["match_history"] = data["match_history"][-50:]

        self.save_player_data()

    def get_statistics(self):
        """Return player statistics."""

        return {
            "total_matches": self.player_data["total_matches"],
            "wins_X": self.player_data["wins_X"],
            "wins_O": self.player_data["wins_O"],
            "draws": self.player_data["draws"],
            "ai_wins": self.player_data["ai_wins"],
            "total_wins": self.player_data["total_wins"],
            "best_streak": self.player_data["best_streak"]
        }

    # ==================================================
    # REPLAY SYSTEM
    # ==================================================

    def record_move(self, index, player):

        self.replay_moves.append({
            "player": player,
            "index": index,
            "board": self.board.copy()
        })

    def save_replay(self):

        self.last_replay = {
            "mode": self.mode,
            "difficulty": self.difficulty,
            "winner": self.winner,
            "moves": [
                {
                    "player": move["player"],
                    "index": move["index"],
                    "board": move["board"].copy()
                }
                for move in self.replay_moves
            ]
        }

    def start_replay(self):
        """Start viewing the last match replay."""

        if not self.last_replay:
            return False

        self.replay_board = [""] * 9
        self.replay_index = 0
        self.replay_active = True

        return True

    def replay_next(self):
        """Move forward one replay step."""

        if not self.replay_active:
            return False

        moves = self.last_replay["moves"]

        if self.replay_index >= len(moves):
            return False

        move = moves[self.replay_index]

        self.replay_board = move["board"].copy()
        self.replay_index += 1

        return True

    def replay_previous(self):
        """Move backward one replay step."""

        if not self.replay_active:
            return False

        if self.replay_index <= 0:
            return False

        self.replay_index -= 1

        if self.replay_index == 0:
            self.replay_board = [""] * 9

        else:
            move = self.last_replay["moves"][
                self.replay_index - 1
            ]

            self.replay_board = move["board"].copy()

        return True

    def replay_first(self):

        if not self.replay_active:
            return False

        self.replay_index = 0
        self.replay_board = [""] * 9

        return True

    def replay_last(self):

        if not self.replay_active:
            return False

        moves = self.last_replay["moves"]

        if not moves:
            return False

        self.replay_index = len(moves)
        self.replay_board = moves[-1]["board"].copy()

        return True

    def stop_replay(self):

        self.replay_active = False
        self.replay_index = 0
        self.replay_board = [""] * 9

    # ==================================================
    # AI PERSONALITY
    # ==================================================

    def set_ai_message(self, message):
        self.ai_message = message

    def get_ai_message(self):
        return self.ai_message

    def ai_reaction_to_player(self):

        reactions = [
            "Interesting move! My turn.",
            "You think you can beat me?",
            "Let me calculate that...",
            "Nice move! But watch this.",
            "I am analysing the board."
        ]

        self.ai_message = random.choice(reactions)

    def ai_reaction_after_move(self):

        if self.game_over:

            if self.winner == "O":
                messages = [
                    "Victory! Better luck next time.",
                    "I told you I was smart!",
                    "AI wins! What a match!"
                ]

            elif self.winner == "X":
                messages = [
                    "You got me this time!",
                    "Impressive! You defeated me.",
                    "Well played. Rematch?"
                ]

            else:
                messages = [
                    "A draw! We are equally matched.",
                    "No winner today!",
                    "What a close match!"
                ]

            self.ai_message = random.choice(messages)

        else:

            messages = [
                "Your move, human!",
                "Let's see what you do next.",
                "I am ready for your next move.",
                "The battle continues!"
            ]

            self.ai_message = random.choice(messages)

    # ==================================================
    # TOURNAMENT SYSTEM
    # ==================================================

    def start_tournament(self, best_of=3):
        """Start a Best of 3 or Best of 5 tournament."""

        if best_of not in (3, 5):
            return False

        self.tournament = {
            "active": True,
            "best_of": best_of,
            "wins": {"X": 0, "O": 0},
            "draws": 0,
            "rounds": 0,
            "champion": None
        }

        self.new_round()

        return True

    def stop_tournament(self):

        self.tournament["active"] = False

    def update_tournament(self, winner):

        tournament = self.tournament

        if not tournament["active"]:
            return

        tournament["rounds"] += 1

        if winner == "Draw":
            tournament["draws"] += 1
        else:
            tournament["wins"][winner] += 1

        required_wins = (
            tournament["best_of"] // 2 + 1
        )

        if tournament["wins"]["X"] >= required_wins:
            tournament["champion"] = "X"
            tournament["active"] = False

        elif tournament["wins"]["O"] >= required_wins:
            tournament["champion"] = "O"
            tournament["active"] = False

        if tournament["champion"]:

            self.ai_message = (
                "Tournament champion: "
                + tournament["champion"]
                + "!"
            )

    def get_tournament_status(self):
        """Return current tournament information."""

        return {
            "active": self.tournament["active"],
            "best_of": self.tournament["best_of"],
            "wins": self.tournament["wins"].copy(),
            "draws": self.tournament["draws"],
            "rounds": self.tournament["rounds"],
            "champion": self.tournament["champion"]
        }

    # ==================================================
    # BOARD MANAGEMENT
    # ==================================================

    def reset_board(self):
        """Reset board without clearing scores."""

        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.moves = 0

        self.replay_moves = []

        self.replay_active = False
        self.replay_index = 0
        self.replay_board = [""] * 9

        self.ai_message = "Let's play! I am ready."

        self._match_recorded = False

    def new_round(self):
        """Start another round while preserving scores."""

        self.reset_board()

    def reset_scores(self):
        """Clear session scores and start fresh."""

        self.score = {
            "X": 0,
            "O": 0,
            "Draw": 0
        }

        self.reset_board()

    # ==================================================
    # SETTINGS
    # ==================================================

    def set_mode(self, mode):

        if mode not in ("AI", "TWO_PLAYER"):
            return

        self.mode = mode
        self.reset_board()

    def set_difficulty(self, difficulty):

        if difficulty not in ("Easy", "Medium", "Hard"):
            return

        self.difficulty = difficulty
        self.reset_board()

    def cycle_difficulty(self):

        levels = ["Easy", "Medium", "Hard"]

        current = levels.index(self.difficulty)

        self.set_difficulty(
            levels[(current + 1) % len(levels)]
        )

    def toggle_sound(self):

        self.sound_on = not self.sound_on

        return self.sound_on

    # ==================================================
    # PLAY MOVE
    # ==================================================

    def play(self, index):
        """Place current player's mark and update game."""

        if self.game_over:
            return False

        if self.replay_active:
            return False

        if not isinstance(index, int) or not 0 <= index < 9:
            return False

        if self.board[index]:
            return False

        player = self.current_player

        self.board[index] = player
        self.moves += 1

        # Record every move for replay
        self.record_move(index, player)

        # Check win/draw
        self._check_result()

        if not self.game_over:

            self.current_player = (
                "O" if player == "X" else "X"
            )

            # AI reaction to human move
            if self.mode == "AI" and player == "X":
                self.ai_reaction_to_player()

        return True

    # ==================================================
    # MATCH RESULT
    # ==================================================

    def _check_result(self):

        if self._match_recorded:
            return

        result = get_winner(tuple(self.board))

        if result:

            self.game_over = True
            self.winner = result

        elif self.moves == 9:

            self.game_over = True
            self.winner = "Draw"

        if self.game_over:

            self._match_recorded = True

            self.score[self.winner] += 1

            # Save replay
            self.save_replay()

            # Update statistics and achievements
            self.update_statistics(self.winner)

            # Update tournament
            self.update_tournament(self.winner)

            # AI personality
            if self.mode == "AI":
                self.ai_reaction_after_move()

    # ==================================================
    # COMPUTER MOVE
    # ==================================================

    def computer_move(self):
        """Make AI move according to selected difficulty."""

        if self.game_over:
            return None

        if self.mode != "AI":
            return None

        if self.current_player != "O":
            return None

        available = empty_cells(self.board)

        if not available:
            return None

        if self.difficulty == "Easy":

            move = random.choice(available)

        elif self.difficulty == "Medium":

            move = medium_move(tuple(self.board))

        else:

            move = best_move(tuple(self.board))

        if move is not None:

            self.play(move)

        return move
