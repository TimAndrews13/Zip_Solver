from grid import zip_solver, StartEnd, print_grid, print_grid_with_solution


def main():
    zipboard = [
        [None, None, None, None, None, None, None],
        [None, 10, 9, None, None, None, None],
        [None, None, 7, None, None, None, None],
        [None, 8, 3, None, 6, 5, None],
        [None, None, None, None, 2, None, None],
        [None, None, None, None, 4, 1, None],
        [None, None, None, None, None, None, None]
    ]
    barriers = [
        {(0, 4), (1, 4)},
        {(0, 5), (1, 5)},
        {(1, 3), (1, 4)},
        {(1, 5), (2, 5)},
        {(2, 3), (2, 4)},
        {(2, 4), (2, 5)},
        {(4, 1), (4, 2)},
        {(4, 2), (4, 3)},
        {(4, 1), (5, 1)},
        {(5, 1), (6, 1)},
        {(5, 2), (5, 3)},
        {(5, 2), (6, 2)},
    ]

    print_grid(zipboard, barriers)

    result = zip_solver(zipboard, barriers)

    print_grid_with_solution(zipboard, barriers, result)

if __name__ == "__main__":
    main()

    