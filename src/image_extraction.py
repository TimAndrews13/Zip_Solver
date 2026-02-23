from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import cv2
import numpy as np
import imutils
import math
import pytesseract


def detect_grid_size(warped_gray, debug=False):
    h, w = warped_gray.shape

    top_half = warped_gray[0:h//2, :]
    grad_x = cv2.Sobel(top_half, cv2.CV_64F, 1, 0, ksize=3)
    grad_x = np.abs(grad_x)

    signal = np.sum(grad_x, axis=0)
    signal = (signal - np.mean(signal)) / (np.std(signal) + 1e-5)

    n = len(signal)
    autocorr = np.correlate(signal, signal, mode='full')[n-1:]

    search_range = autocorr[30:w//4]
    if len(search_range) == 0:
        return 7

    cell_width = np.argmax(search_range) + 30
    estimated_N = round(w / cell_width)

    if debug:
        print(f"[DEBUG] Detected Cell Width (Rhythm): {cell_width}px")
        print(f"[DEBUG] W: {w}, Calculated N: {estimated_N}")

    if 4 <= estimated_N <= 10:
        return estimated_N

    return 7


def find_grid(image, debug=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 3)

    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
        11, 2)
    thresh = cv2.bitwise_not(thresh)

    if debug:
        cv2.imshow("Puzzle Thresh", thresh)
        cv2.waitKey(0)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    gridCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            gridCnt = approx
            break

    if gridCnt is None:
        raise Exception("Could not find Zip Puzzle Outline")

    if debug:
        output = image.copy()
        cv2.drawContours(output, [gridCnt], -1, (0, 255, 0), 2)
        cv2.imshow("Puzzle Outline", output)
        cv2.waitKey(0)

    grid   = four_point_transform(image, gridCnt.reshape(4, 2))
    warped = four_point_transform(gray,  gridCnt.reshape(4, 2))

    N = detect_grid_size(warped, debug=debug)

    if debug:
        print(f"[DEBUG] Detected a {N}x{N} grid.")
        cv2.imshow("Puzzle Transform", grid)
        cv2.waitKey(0)

    return (grid, warped, N)


def find_numbers(cell, debug=False):
    if len(cell.shape) == 3:
        cell = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

    h, w = cell.shape
    margin_h, margin_w = int(h * 0.2), int(w * 0.2)
    center_cell = cell[margin_h:h-margin_h, margin_w:w-margin_w]

    _, thresh = cv2.threshold(center_cell, 80, 255, cv2.THRESH_BINARY_INV)

    if cv2.countNonZero(thresh) < 20:
        return None

    _, digit = cv2.threshold(center_cell, 150, 255, cv2.THRESH_BINARY)
    digit = clear_border(digit)

    return digit


def find_barriers(warped, N, debug=False):
    """
    Detect barrier walls between adjacent cells in the warped grid image.

    Returns a list of sets, each set containing the two (row, col) cell coordinates
    that share the barrier edge, e.g. {(1, 3), (2, 3)}.
    """
    h, w = warped.shape[:2] if len(warped.shape) == 3 else warped.shape
    stepY = h / N
    stepX = w / N

    half_strip = 4
    THRESHOLD = 0.25

    barriers = []

    # Horizontal barriers: between cell (r, c) and (r+1, c)
    for r in range(N - 1):
        edge_y = int((r + 1) * stepY)
        y1 = max(0, edge_y - half_strip)
        y2 = min(h, edge_y + half_strip)

        for c in range(N):
            x1 = int(c * stepX) + 2
            x2 = int((c + 1) * stepX) - 2

            strip = warped[y1:y2, x1:x2]
            dark_ratio = np.sum(strip < 80) / max(strip.size, 1)

            if dark_ratio > THRESHOLD:
                barriers.append({(r, c), (r + 1, c)})
                if debug:
                    print(f"[DEBUG] Horizontal barrier ({r},{c})-({r+1},{c})  dark={dark_ratio:.2f}")

    # Vertical barriers: between cell (r, c) and (r, c+1)
    for c in range(N - 1):
        edge_x = int((c + 1) * stepX)
        x1 = max(0, edge_x - half_strip)
        x2 = min(w, edge_x + half_strip)

        for r in range(N):
            y1 = int(r * stepY) + 2
            y2 = int((r + 1) * stepY) - 2

            strip = warped[y1:y2, x1:x2]
            dark_ratio = np.sum(strip < 80) / max(strip.size, 1)

            if dark_ratio > THRESHOLD:
                barriers.append({(r, c), (r, c + 1)})
                if debug:
                    print(f"[DEBUG] Vertical barrier ({r},{c})-({r},{c+1})  dark={dark_ratio:.2f}")

    return barriers


def extract_puzzle(image_path, debug=False):
    """
    Full pipeline: given a path to a Zip puzzle image, return the board and barriers.

    Returns:
        board    -- NxN numpy int array, 0 = empty cell, >0 = numbered cell
        barriers -- list of sets, each {(r1,c1), (r2,c2)} is a wall between two cells
        N        -- grid size

    Example:
        board, barriers, N = extract_puzzle("puzzle.png")
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    image = imutils.resize(image, width=600)
    (gridImage, warped, N) = find_grid(image, debug=debug)

    board = np.zeros((N, N), dtype="int")
    stepX = warped.shape[1] / N
    stepY = warped.shape[0] / N

    for y in range(N):
        for x in range(N):
            startX = int(x * stepX)
            startY = int(y * stepY)
            endX   = int((x + 1) * stepX)
            endY   = int((y + 1) * stepY)

            cell  = warped[startY:endY, startX:endX]
            digit = find_numbers(cell, debug=debug)

            if digit is not None:
                cnts = cv2.findContours(digit.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)

                if len(cnts) > 0:
                    all_x, all_y, all_x2, all_y2 = [], [], [], []
                    for c in cnts:
                        dx, dy, dw, dh = cv2.boundingRect(c)
                        all_x.append(dx);       all_y.append(dy)
                        all_x2.append(dx + dw); all_y2.append(dy + dh)
                    digit = digit[min(all_y):max(all_y2), min(all_x):max(all_x2)]

                ocr_input = cv2.bitwise_not(digit)
                ocr_input = cv2.resize(ocr_input, None, fx=8, fy=8, interpolation=cv2.INTER_CUBIC)
                _, ocr_input = cv2.threshold(ocr_input, 180, 255, cv2.THRESH_BINARY)
                kernel    = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
                ocr_input = cv2.dilate(ocr_input, kernel, iterations=1)
                ocr_input = cv2.copyMakeBorder(ocr_input, 40, 40, 40, 40,
                                               cv2.BORDER_CONSTANT, value=255)

                if debug:
                    cv2.imwrite(f"debug_cell_{y}_{x}.png", ocr_input)

                config = "--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789"
                text   = pytesseract.image_to_string(ocr_input, config=config).strip()
                if not text.isdigit():
                    config = "--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789"
                    text   = pytesseract.image_to_string(ocr_input, config=config).strip()

                if debug:
                    print(f"[DEBUG] Cell ({y},{x}) OCR: '{text}'")

                if text.isdigit():
                    board[y, x] = int(text)

    barriers = find_barriers(warped, N, debug=debug)

    return board, barriers, N