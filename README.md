# Chess

A fully playable chess game built with Python and Pygame, featuring a human vs AI mode. The game implements all standard chess rules with a clean drag-and-drop interface.

## Features

- **All standard moves** — normal piece movement for all six piece types
- **Special moves** — en passant, castling (king-side and queen-side for both colors), and pawn promotion with a piece-selection overlay
- **Board perspective** — choose to play as White or Black at startup; the board flips automatically so your pieces are always at the bottom
- **Check detection** — the king's square is highlighted in red when in check
- **Checkmate & stalemate detection** — game ends automatically with a result banner
- **Draw rules** — threefold repetition and the 50-move rule are both enforced
- **Touch-move rule** — once you pick up a piece, you must place it on a legal square
- **Move animation** — the AI's chosen piece slides smoothly to its destination before the board updates
- **AI opponent** — plays the opposite color using minimax with alpha-beta pruning and the following evaluation:
  - Material scoring (standard piece values)
  - Piece-square tables for all six piece types (positional awareness)
  - King safety bonus for retaining castling rights
  - Search depth of 4 half-moves (plies)

## Controls

| Action | Input |
|---|---|
| Choose color | Press **W** (White) or **B** (Black) at the start screen |
| Pick up a piece | Click and hold |
| Place a piece | Release mouse button |

Legal move destinations are shown as highlighted circles when a piece is picked up. Castling destinations are shown separately for the king.

When a pawn reaches the back rank, a promotion overlay appears in the center of the board — click the desired piece (queen, rook, bishop, or knight) to complete the promotion.

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
├── game_UI.py            # Pygame window, event loop, rendering, animation
├── board.py              # Board state, move generation, check/castle logic, make/unmake for AI
├── move.py               # Move representation
├── SmartMoveFinder.py    # AI move selection (minimax with alpha-beta pruning)
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

**Board representation.** The board uses a 120-element mailbox array (10×12) with sentinel `'x'` squares around the border to simplify out-of-bounds detection during move generation. White pieces are uppercase (`K`, `Q`, `R`, `B`, `N`, `P`) and black pieces are lowercase (`k`, `q`, `r`, `b`, `n`, `p`). Empty squares are `'-'`.

**Move legality.** Pseudo-legal moves are generated first, then each is tested by applying it on the board and checking whether the moving side's king is left in check. Castling legality additionally verifies that the king does not pass through or land on an attacked square.

**Make/unmake system.** The AI uses an incremental make/unmake approach (`make_ai_move` / `unmake_ai_move`) that pushes only the changed flags (en passant target, castling rights, half-move counter, and the move object itself) onto a stack rather than copying the entire board array, making the search significantly faster.

**AI search.** The minimax search (`MinMax_recursive` in `SmartMoveFinder.py`) runs to a fixed depth of 4 plies with alpha-beta pruning. Move order is randomized before each search so equally scored lines vary between games. The static evaluator sums material values and piece-square table bonuses for all pieces on the board, and adds a small bonus for each side that still retains castling rights.

**Window scaling.** On startup, `game_UI.py` reads the display height and sizes the board to 85% of the screen height, keeping the UI sharp at any resolution. On Windows, DPI scaling is explicitly disabled via `ctypes` to prevent blurry rendering.

**Threefold repetition hashing.** After every move the board is serialised to a string (piece layout + en passant target + castling flags + side to move) and stored in a dictionary; a draw is declared when any position reaches a count of three.
