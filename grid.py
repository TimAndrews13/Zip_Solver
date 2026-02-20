import copy


zipArray = [
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





'''PsuedoCode for Zip Solver using backtracking
1. Set the Starting Point to 1
2. Make sure the neighbors of 1 do not validate path constraints
    a. Neighbor must be on the grid
    b. Neighbor cannot be on the other side of a barrier
    c. If the neighbor is a numbered cell, than it must be 1 more than the last number found
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


start, end = StartEnd(zipArray)
height = len(zipArray)
width = len(zipArray[0])
total_cells = height * width
current_number = 1

#Going to start at Start Number of 1, Start Location of start variable, and current path of [start]

if start == end:
    print("Full Path Complete")
else:
    for x, y in [[1,0], [0,1], [-1,0], [0,-1]]:
        new_x = start[0] + x 
        new_y = start[1] + y
        new_location = (new_x, new_y)
        if 0 <= new_x < height and 0 <= new_y < width:
            print(f"New Location {new_location} Is on the Board!")
            if new_location not in barriers:
                print(f"No Barrier in the way of New Location {new_location}!")
                if zipArray[new_x][new_y] is None or zipArray[new_x][new_y] == current_number + 1:
                    print(f"New Location {new_location} is Valid!")
                else:
                    print(f"New Locaiton {new_location} is not the Next Number")
            else:
                print(f"Barrier blocks this path")
        else:
            print(f"New Location {new_location} not on the board")