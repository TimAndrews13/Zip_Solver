from zip_solve import zip_solver
from grid import print_grid, print_grid_with_solution
from image_extraction import extract_puzzle


def main():
    zipboard, barriers, N = extract_puzzle("/home/tim_andrews/workspace/timandrews/Zip_Solver/src/test_image2.png")

    zipboard = [[int(v) if v != 0 else None for v in row] for row in zipboard]

    print_grid(zipboard, barriers)

    result = zip_solver(zipboard, barriers)

    print_grid_with_solution(zipboard, barriers, result)

if __name__ == "__main__":
    main()

    