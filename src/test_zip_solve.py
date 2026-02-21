import unittest

from grid import zip_solver

class TestZipSolve(unittest.TestCase):
    def test_ZipPuzzle1(self):
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
        answer = [(5, 5), (4, 5), (4, 4), (4, 3), (3, 3), (3, 2), (4, 2), (5, 2), (5, 1), (5, 0), (6, 0), (6, 1), (6, 2), (6, 3), (5, 3), (5, 4), (6, 4), (6, 5), (6, 6), (5, 6), (4, 6), (3, 6), (2, 6), (2, 5), (3, 5), (3, 4), (2, 4), (1, 4), (1, 5), (1, 6), (0, 6), (0, 5), (0, 4), (0, 3), (1, 3), (2, 3), (2, 2), (2, 1), (3, 1), (4, 1), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2), (1, 1)]
        self.assertEqual(answer, zip_solver(zipboard, barriers))

    def test_ZipPuzzle2(self):
        zipboard = [
            [None, None, None, None, None, None, None],
            [None, 14, None, 3, None, 8, None],
            [1, None, 4, None, 2, None, 9],
            [None, None, None, None, None, None, None],
            [13, None, 5, None, 12, None, 10],
            [None, 6, None, 7, None, 11, None],
            [None, None, None, None, None, None, None],
        ]
        barriers = []
        answer = [(2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (2, 3), (1, 3), (1, 2), (2, 2), (3, 2), (4, 2), (4, 1), (5, 1), (5, 2), (5, 3), (4, 3), (3, 3), (3, 4), (3, 5), (2, 5), (1, 5), (0, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (6, 5), (5, 5), (4, 5), (4, 4), (5, 4), (6, 4), (6, 3), (6, 2), (6, 1), (6, 0), (5, 0), (4, 0), (3, 0), (3, 1), (2, 1), (1, 1)]
        self.assertEqual(answer, zip_solver(zipboard, barriers))

    def test_ZipPuzzle3(self):
        zipboard = [
            [None, None, 9, 10, None, None],
            [None, 14, 11, None, None, None],
            [8, 13, None, None, None, 1],
            [7, None, None, None, 3, 2],
            [None, None, None, 12, 4, None],
            [None, None, 6, 5, None, None]
        ]
        barriers = []
        answer = [(2, 5), (3, 5), (3, 4), (4, 4), (4, 5), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (1, 4), (2, 4), (2, 3), (1, 3), (1, 2), (2, 2), (3, 2), (3, 3), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1), (1, 1)]
        self.assertEqual(answer, zip_solver(zipboard, barriers))

if __name__ == "__main__":
    unittest.main()