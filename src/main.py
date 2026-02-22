from zip_solve import zip_solver
from grid import print_grid, print_grid_with_solution


def main():
    zipboard = [
        [None, None, None, None, None, None, None],
        [None, 3, None, 2, None, 1, None],
        [None, None, None, None, 6, None, None],
        [None, 5, None, None, None, 7, None],
        [None, None, 4, None, None, None, None],
        [None, 9, None, 10, None, 8, None],
        [None, None, None, None, None, None, None]
    ]
    barriers = [
        {(1, 1), (2, 1)},
        {(1, 3), (2, 3)},
        {(1, 5), (2, 5)},
        {(1, 6), (2, 6)},
        {(2, 3), (3, 3)},
        {(2, 5), (3, 5)},
        {(3, 1), (4, 1)},
        {(3, 3), (4, 3)},
        {(4, 0), (5, 0)},
        {(4, 1), (5, 1)},
        {(4, 3), (5, 3)},
        {(4, 5), (5, 5)},
    ]

    print_grid(zipboard, barriers)

    result = zip_solver(zipboard, barriers)

    print_grid_with_solution(zipboard, barriers, result)

if __name__ == "__main__":
    main()

    