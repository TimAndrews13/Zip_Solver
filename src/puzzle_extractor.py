"""
new_python.py — CLI wrapper for extract_puzzle().

Run:
    python new_python.py -i puzzle.png
    python new_python.py -i puzzle.png -d 1   # debug mode

To use in main.py instead:
    from image_extraction import extract_puzzle
    board, barriers, N = extract_puzzle("puzzle.png")
"""

from image_extraction import extract_puzzle
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",  required=True, help="path to input Zip puzzle image")
ap.add_argument("-d", "--debug",  type=int, default=-1, help="visualize pipeline (1 = on)")
args = vars(ap.parse_args())

board, barriers, N = extract_puzzle(args["image"], debug=args["debug"] > 0)

print(f"\n[INFO] Detected a {N}x{N} grid.")
print("\n[INFO] Board:")
print(board)
print("\n[INFO] Barriers:")
for b in sorted(barriers, key=lambda s: sorted(s)):
    print(f"    {b},")