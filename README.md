<<<<<<< HEAD
# 🎮 Tic-Tac-Toe AI — Python Quest

A neon-themed Tic-Tac-Toe desktop game built with Python and Pygame. Play as **X** against an unbeatable computer opponent playing **O**.

## Features
- Clean neon cyan and purple interface
- Human vs AI gameplay
- Minimax AI (the computer will never lose)
- Scoreboard for wins, AI wins, and draws
- New Round and Reset Scores controls
- Separated game logic and UI code

## Requirements
- Python 3.10+
- Pygame 2.5+

## Run on Windows (VS Code terminal)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If activation is blocked in PowerShell, open Command Prompt in VS Code and run:

```bat
.venv\Scripts\activate.bat
```

Then install requirements and run `python main.py`.

## How to play
1. You play as **X** and go first.
2. Click an empty square.
3. The AI responds as **O**.
4. Make three marks in a row, column, or diagonal to win.
5. Click **NEW ROUND** to play again without clearing scores.
6. Click **RESET SCORES** to clear the scoreboard and start fresh.

## How the AI works
The AI uses the **Minimax algorithm**. It checks possible future moves and chooses the move with the best outcome. It plays optimally, so it cannot be beaten; the best possible result against it is a draw.

## Project structure

```text
tictactoe-pygame/
├── main.py
├── game.py
├── ui.py
├── requirements.txt
├── README.md
├── tests/
└── assets/
```

## Learning concepts
- Lists and indexing
- Functions and modules
- Classes and objects
- Conditional logic
- Event handling with Pygame
- Recursion and the Minimax algorithm
=======
# Neon-Cyberpunk-TicTacToe
A futuristic Tic-Tac-Toe game built with Python and Pygame, featuring Minimax AI, achievements, replay and tournaments.
>>>>>>> 4cf8282d9ab7f423b9d7fa4f75c44a2caa1855af
