import time

def isMovevalid(board, row, col):
    if row >= 0 and row < len(board) and col >= 0 and col < len(board) and board[row][col] == 0:
        return True
    else:
        return False

def knightTour(board, row, col, step, m, count):
    xWalk = [2, 1, -1, -2, -2, -1, 1, 2]
    yWalk = [1, 2, 2, 1, -1, -2, -2, -1]

    # Count the child of the root
    validMoves = []
    for i in range(len(xWalk)):
        nextX = row + xWalk[i]
        nextY = col + yWalk[i]

        if isMovevalid(board, nextX, nextY):
            validMoves.append([nextX, nextY])
    

    if step[0] == (len(board)*len(board)):
        row = 0
        print("Row")
        for i in board:
            print(f"{row}\t{i}")
            row += 1
        # print("This is the valid moves")
        # print(validMoves)
        print("\nThis is the m list")
        print(m)
        return True

    print(f"Visiting step {step} at position ({row}, {col})")

    for nextX, nextY in validMoves:
        step[0] += 1
        board[nextX][nextY] = step[0]
        count[0] += 1

        m.append(len(validMoves))

        if knightTour(board, nextX, nextY, step, m, count):
            return True
        
        step[0] -= 1
        board[nextX][nextY] = 0
        m.pop()
    return False
    

def est_tree_size(m):
    total = [1]
    product = 1
    for i in m:
        product *= i
        total.append(product)
    return total

def urutan(board, m):
    n = len(board)
    totalStep = len(m)+1

    # Search urutan langkah
    step = []
    count = 1
    while count <=totalStep:
        for i in range(n):
            for j in range(n):
                if board[i][j] == count:
                    step.append([i,j])
                    count += 1
    return step

# Generate NxN chess board
n = int(input("Insert the width & length of the chess board (N x N) = "))

board = []
for x in range(n):
    row = []
    for y in range(n):
        row.append(0)
    board.append(row)

row = 0
print("Row")
for i in board:
    print(f"{row}\t{i}")
    row += 1


# input section
print("Select a box to start the knight tour ")
x = int(input("\nInsert the x-axis (must be a number) = "))
y = int(input("\nInsert the y-axis (must be a number) = "))

# Start time searching
start_time = time.time()

m = []
count = [0]
step = [1]

# Start node
board[x][y] = step[0]
knightTour(board, x, y, step, m, count)

steps = urutan(board, m)
    

# # Calculate the product of each items in m
# size = est_tree_size(m)

# print(f"The tree size is {sum(size):,}")

end_time = time.time()
duration = end_time - start_time
print(f"To execute this program takes {duration}")