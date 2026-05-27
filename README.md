# Chess

A fully playable chess game built with Python and Pygame, featuring a human vs AI mode. The game implements all standard chess rules with a clean drag-and-drop interface.

## Features

- **All standard moves** — normal piece movement for all six piece types
- **Special moves** — en passant, castling (king-side and queen-side for both colors), and pawn promotion with piece selection UI
- **Check detection** — the king's square is highlighted in red when in check
- **Checkmate & stalemate detection** — game ends automatically with a result banner
- **Draw rules** — threefold repetition and 50-move rule are both enforced
- **Touch-move rule** — once you pick up a piece, you must move it
- **AI opponent** — plays as Black using a minimax search with the following evaluation:
  - Material scoring (standard piece values)
  - Piece-square tables for all six piece types (positional awareness)
  - King safety bonus for retaining castling rights
  - Three selectable AI modes: **Smart** (minimax), **Greedy** (best immediate capture), **Random**

## Controls

| Action | Input |
|---|---|
| Pick up a piece | Click and hold |
| Place a piece | Release mouse button |

Legal move destinations are shown as highlighted circles when a piece is picked up. Castle destinations are shown separately for the king.

## Requirements

- Python 3.x
- Pygame
- NumPy

Install dependencies with:

```bash
pip install pygame numpy
```

## Project Structure

```
├── game_UI.py            # Pygame window, event loop, rendering
├── board.py              # Board state, move generation, check/castle logic
├── move.py               # Move representation
├── SmartMoveFinder.py    # AI move selection (minimax, greedy, and random modes)
└── Chess_images/         # SVG piece assets (king, queen, rook, bishop, knight, pawn — black & white)
```

## Running the Game

Run the following command from the same directory as `game_UI.py`:

```bash
python game_UI.py
```

Make sure the `Chess_images/` folder is in the same directory as the scripts.

If dependencies aren't found or the game doesn't launch, set up a virtual environment first:

```bash
python -m venv my_env
source my_env/bin/activate  # On Windows: my_env\Scripts\activate
pip install pygame numpy
python game_UI.py
```

## Implementation Notes

The board uses a **120-element mailbox array** (10×12) with sentinel `'x'` squares around the border to simplify out-of-bounds detection during move generation. White pieces are uppercase (`K`, `Q`, `R`, `B`, `N`, `P`) and black pieces are lowercase (`k`, `q`, `r`, `b`, `n`, `p`). Empty squares are `'-'`.

Move legality is determined in two stages: pseudo-legal moves are generated first, then each is tested by applying it on the board and checking whether the moving side's king is left in check.

The AI uses an incremental make/unmake system (`make_ai_move` / `unmake_ai_move`) that pushes only the changed flags onto a stack rather than copying the entire board, making the search significantly faster. The minimax evaluator scores positions using piece values, piece-square tables for all piece types, and a small bonus for retaining castling rights.
