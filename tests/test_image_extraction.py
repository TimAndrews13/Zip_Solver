import unittest
from pathlib import Path
from zip_solve import zip_solver
from image_extraction import extract_puzzle

IMAGES_DIR = Path(__file__).parent / "images"

class TestZipSolve(unittest.TestCase):
    def test_ZipPuzzle_Image_1(self):
        zipboard, barriers, N = extract_puzzle(str(IMAGES_DIR / "test_image.png"))
        zipboard = [[int(v) if v != 0 else None for v in row] for row in zipboard]
        answer = [(5, 5), (4, 5), (4, 4), (4, 3), (3, 3), (3, 2), (4, 2), (5, 2), (5, 1), (5, 0), (6, 0), (6, 1), (6, 2), (6, 3), (5, 3), (5, 4), (6, 4), (6, 5), (6, 6), (5, 6), (4, 6), (3, 6), (2, 6), (2, 5), (3, 5), (3, 4), (2, 4), (1, 4), (1, 5), (1, 6), (0, 6), (0, 5), (0, 4), (0, 3), (1, 3), (2, 3), (2, 2), (2, 1), (3, 1), (4, 1), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2), (1, 1)]
        self.assertEqual(answer, zip_solver(zipboard, barriers))

    def test_ZipPuzzle_Image_2(self):
        zipboard, barriers, N = extract_puzzle(str(IMAGES_DIR / "test_image1.png"))
        zipboard = [[int(v) if v != 0 else None for v in row] for row in zipboard]
        answer = [(2, 5), (3, 5), (3, 4), (4, 4), (4, 5), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (1, 4), (2, 4), (2, 3), (1, 3), (1, 2), (2, 2), (3, 2), (3, 3), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1), (1, 1)]
        self.assertEqual(answer, zip_solver(zipboard, barriers))

    def test_ZipPuzzle_Image_3(self):
        zipboard, barriers, N = extract_puzzle(str(IMAGES_DIR / "test_image2.png"))
        zipboard = [[int(v) if v != 0 else None for v in row] for row in zipboard]
        answer = [(4, 1), (4, 2), (3, 2), (2, 2), (1, 2), (1, 1), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (2, 5), (3, 5), (3, 4), (2, 4), (1, 4), (1, 3), (2, 3), (3, 3), (4, 3), (4, 4), (4, 5), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (5, 0), (4, 0), (3, 0), (3, 1), (2, 1), (2, 0)]
        self.assertEqual(answer, zip_solver(zipboard, barriers))

if __name__ == "__main__":
    unittest.main()