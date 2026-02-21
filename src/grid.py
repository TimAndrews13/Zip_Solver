import copy
from pprint import pprint

'''PsuedoCode for Zip Solver using backtracking
1. Set the Starting Point to 1
2. Make sure the neighbors of 1 do not validate path constraints
    a. Neighbor must be on the grid
    b. Neighbor cannot be on the other side of a barrier
    c. If the neighbor is a numbered cell, than it must be 1 more than the last number found
    d. All cells must be visited once
3. For each neighbor that does not validate contraints, update the parameters and recursively call the function
4. If the Last number is reached, then path is completed, and you can return
'''

def StartEnd(board):
    height = len(board)
    width = len(board[0])
    total_cells = height * width
    start_number = 1
    end_number = -float("inf")

    for x in range(height):
        for y in range(width):
            if board[x][y] is not None:
                if board[x][y] == start_number:
                    start_location = (x, y)
                elif board[x][y] > end_number:
                    end_number = board[x][y]
                    end_location = (x, y)

    return start_location, end_location


#Define Recursive Function to Solve Zip Board
#Parameters will be the Current Number (will start with 1), Postion of 1, and Current Path

def zip_solver(board, barriers):
    start, end = StartEnd(board)
    height = len(board)
    width = len(board[0])
    total_cells = height * width
    path = []

    #Helper Funciton to Print Grid Evenly
    def print_grid_with_barriers(board, barriers):
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

    print_grid_with_barriers(board, barriers)
    
    def backtrack_function(current_number, current_position, current_path):
        '''
        Base Case: Check if The Current Location is Equal to the End Position
        Then Check to see if the lenght of the Current Path is Equal to the Number of Cells on the Board
        If both are true, then the puzzle is solved and function exits recurssion
        '''
        if current_position == end:
            if len(current_path) == total_cells:
                path.append(current_path.copy())
                print(f"Full Path Complete")
                return current_path.copy()

        '''
        For the Current Location, Funciton Must Evaluate all Neighbors for Validity
        -New Location Must Be on the Board
        -New Location Cannot Pass Through a Barrier (Barrier is defined by a set of adjacent Locations)
        -New Location must have a None Value, or be One More than the Current Number
        '''

        #print(f"Current Position is {current_position}")

        #Create New Neighbor Locations By adding/subtracting 1 from either the x or y coordinate
        for x, y in [[1,0], [0,1], [-1,0], [0,-1]]:
            #Set Variables for New Neighbor to Check
            new_x = current_position[0] + x 
            new_y = current_position[1] + y
            new_location = (new_x, new_y)

            #print(f"Checking Location {new_location}")
            '''
            First Check is to see fi the New Location has already been visited.  To do this check if New Location is already in the Current Path.  If it go to the next iterable by continuing.
            '''
            if new_location in current_path:
                #print(f"New Location {new_location} in Current Path {current_path}")
                continue
            '''
            Second Check to see if the New Location is on the Board
            -New X must be greater than or equal to 0 and less than the height of the board
            -New Y must be greater than or equal to 0 and less than the width of the board
            '''
            if 0 <= new_x < height and 0 <= new_y < width:
                
                #print(f"New Location {new_location} on Board")

                '''
                Third Check to see if New Location passes through a Barrier
                '''
                if {current_position, new_location} not in barriers:
                    
                    #print(f"New Location {new_location} Does not Pass Barrier")

                    '''
                    Fourth Check to see if New Location has a Number... 
                    '''
                    if board[new_x][new_y] is not None:

                        #print(f"New Location {new_location} has Number...")
                        '''
                        ...and if it does if that Number is 1 more than the Current Number
                        '''
                        if board[new_x][new_y] != current_number + 1:
                            continue

                            #print(f"New Location has Number {current_number + 1} The next Number!")
                            #print(f"Adding {new_location} to {current_path}")
                            #print(f"Path is now {current_path + new_path}")
                            '''
                            If the New Location has the Next Number, We can recursively call the function on the Next Number (Current Number + 1), the New Location, and then the Current Path + New Path (New Location as a List)
                            '''

                            #print(f"Recursively calling backtrack_function on New Number {current_number}, New Location {new_location}, and New Path {current_path + new_path}")

                        result = backtrack_function(current_number + 1, new_location, current_path + [new_location])
                    elif board[new_x][new_y] is None:
                        result = backtrack_function(current_number, new_location, current_path + [new_location])
                    if result:
                        return result
        return None

    return backtrack_function(1, start, [start])
     

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

zip_solver(zipboard, barriers)