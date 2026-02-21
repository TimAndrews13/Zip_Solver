
#Function to Print Grid before Solving
def print_grid(board, barriers):
    rows = len(board)
    cols = len(board[0] if rows > 0 else 0)

    CELL_W = 4
    WALL_W = 3

    for r in range(rows):
        row_str = ""
        for c in range(cols):
            val = str(board[r][c] if board[r][c] is not None else 0)
            row_str += val.center(CELL_W)

            if c < cols - 1:
                if {(r,c), (r, c + 1)} in barriers:
                    row_str += "|".center(WALL_W)
                else:
                    row_str += " ".center(WALL_W)
        print(row_str)

        if r < rows -1:
            divider_str = ""
            for c in range(cols):
                if {(r,c), (r + 1, c)} in barriers:
                    divider_str += "---".center(CELL_W)
                else:
                    divider_str += " ".center(CELL_W)
                divider_str += " ".center(WALL_W)
            print(divider_str)


#Funciton to Print Grid After Solving
def print_grid_with_solution(board, barriers, path):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    step_lookup = {coord: i + 1 for i, coord in enumerate(path)}

    max_step = len(path)
    cell_w = max(len(str(max_step)), 2) + 2
    wall_w = 3

    for r in range(rows):
        row_str = ""
        for c in range(cols):
            if (r, c) in step_lookup:
                val = str(step_lookup[(r, c)])
            elif data[r][c] is not None:
                val = str(data[r][c])
            else:
                val = "0"

            row_str += val.center(cell_w)

            if c < cols - 1:
                if {(r, c), (r, c + 1)} in barriers:
                    row_str += "|".center(wall_w)
                else:
                    row_str += " ".center(wall_w)
        print(row_str)

        if r < rows - 1:
            div_str = ""
            for c in range(cols):
                if {(r, c), (r + 1, c)} in barriers:
                    div_str += ("-" * (cell_w - 1)).center(cell_w)
                else:
                    div_str += " ".center(cell_w)
                div_str += " ".center(wall_w)
            print(div_str)