# Zip Solver

For my first python project through the [boot.dev](https://www.boot.dev) Back-End Developer Path, I wanted to figure out a programatic way to solve the [LinkedIn Zip puzzle](https://www.linkedin.com/games/zip/).  A couple years back, LinkedIn started publishing daily puzzles that my fiance and I love to complete and compete against each other.  I think this might give me a leg up!

When fed a screenshot of the puzzle, this pipeline will detect the game grid, read the numbered cells, identify the barriers that cannot be passed, and figure out the solution path using a backtracking algorithm.

---

## How It Works

1. **Grid detection** — finds and perspective-corrects the puzzle grid using OpenCV contour detection
2. **Number extraction** — reads each numbered cell using Tesseract OCR
3. **Barrier detection** — identifies thick wall segments between cells by measuring dark pixel density along cell edges
4. **Solving** — uses backtracking to find a valid Hamiltonian path that visits every cell on the board, and visits the numbered cells in order

---

## Future Updates

There are a few future updates that I would like to make to this repo.  Feel free to clone this repo and push commits if you think you are up for the challenge to add and implement any of these future enhancements.  I am open to other enhancements as well!

1. **Image Screenshots From LinkedIn** - Take a screenshot from [LinkedIn Zip puzzle](https://www.linkedin.com/games/zip/) to generate the image automatically
2. **Any Zip Puzzle from Any Source** - Update functions in image_extraction.py to support puzzle images from any source, not just [LinkedIn Zip puzzle](https://www.linkedin.com/games/zip/)
3. **Cell Color Recognition** - Update image_extraction.py to support non-black and white color extaction
4. **Cleaner Grid Print to Command Line Output** - Update grid.py to print the Grid Cleaner.  Options include printing the grid lines and printing the actual solve pad instead of the indicies visited.

---

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

Install Tesseract on Ubuntu/Debian:
```bash
sudo apt install tesseract-ocr
```

---

## Setup

**With uv (recommended):**
```bash
git clone https://github.com/TimAndrews13/Zip_Solver.git
cd Zip_Solver
uv sync
```

**With pip:**
```bash
git clone https://github.com/TimAndrews13/Zip_Solver.git
cd Zip_Solver
pip install -r requirements.txt
```

---

## Usage

```bash
uv run python src/main.py -i path/to/your/puzzle.png
```

With debug output (saves per-cell OCR images and prints barrier detection details):
```bash
uv run python src/main.py -i path/to/your/puzzle.png -d
```

Or via the shell script:
```bash
./main.sh tests/images/test_image.png
```

---

## Example

**Input:**

![Zip puzzle input](tests/images/test_image.png)

**Output:**
```
 0      0      0      0      0      0      0
                            ---    ---
 0      10     9      0   |  0      0      0
                                   ---
 0      0      7      0   |  0   |  0      0

 0      8      3      0      6      5      0

 0      0   |  0   |  0      2      0      0
       ---
 0      0      0   |  0      4      1      0
       ---    ---
 0      0      0      0      0      0      0

---------------------------------
Zips Puzzle Completed
---------------------------------

 45     46     47     34     33     32     31
                            ---    ---
 44     49     48     35  |  28     29     30
                                   ---
 43     38     37     36  |  27  |  24     23

 42     39     6      5      26     25     22

 41     40  |  7   |  4      3      2      21
       ---
 10     9      8   |  15     16     1      20
       ---    ---
 11     12     13     14     17     18     19
```

---

## Project Structure

```
Zip_Solver/
├── src/
│   ├── main.py                     # Entry point — runs full pipeline
│   ├── image_extraction.py         # CV pipeline: grid detection, OCR, barrier detection
│   ├── zip_solve.py                # Backtracking solver
│   └── grid.py                     # Grid printing utilities
├── tests/
│   ├── images/                     # Sample puzzle images
│   ├── test_image_extraction.py    # Image Extraction and Solver unit tests
│   └── test_zip_solve.py           # Solver unit tests
├── main.sh                         # Shell script shortcut
├── pyproject.toml
└── README.md
```

---

## Running Tests

```bash
uv run python -m pytest tests/
```