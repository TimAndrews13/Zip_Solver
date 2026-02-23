import copy

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
    
    def backtrack_function(current_number, current_position, current_path):
        '''
        Base Case: Check if The Current Location is Equal to the End Position
        Then Check to see if the lenght of the Current Path is Equal to the Number of Cells on the Board
        If both are true, then the puzzle is solved and function exits recurssion
        '''
        if current_position == end:
            if len(current_path) == total_cells:
                path.append(current_path.copy())
                print("---------------------------------")
                print("Zips Puzzle Completed")
                print("---------------------------------")
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
                        if board[new_x][new_y] != current_number + 1:
                            continue                          # ← was outside this block before
                        result = backtrack_function(current_number + 1, new_location, current_path + [new_location])
                    elif board[new_x][new_y] is None:
                        result = backtrack_function(current_number, new_location, current_path + [new_location])
                    if result:
                        return result
        return None

    return backtrack_function(1, start, [start])
