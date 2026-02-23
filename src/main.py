from zip_solve import zip_solver
from grid import print_grid, print_grid_with_solution
from image_extraction import extract_puzzle
import argparse
import os


def main():
    ap = argparse.ArgumentParser(description="Solve a LinkedIn Zip puzzle from an image.")
    ap.add_argument("-i", "--image", required=True, help="path to input Zip puzzle image")
    ap.add_argument("-d", "--debug", action="store_true", help="enable debug output")
    args = vars(ap.parse_args())
    args["image"] = os.path.abspath(args["image"])

    zipboard, barriers, N = extract_puzzle(args["image"], debug=args["debug"])

    zipboard = [[int(v) if v != 0 else None for v in row] for row in zipboard]

    print_grid(zipboard, barriers)

    result = zip_solver(zipboard, barriers)

    if result is None:
        print("[ERROR] No solution found.")
        return

    print_grid_with_solution(zipboard, barriers, result)


if __name__ == "__main__":
    main()
    