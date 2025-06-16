import tkinter as tk

def isMovevalid(board, row, col):
    if row >= 0 and row < len(board) and col >= 0 and col < len(board) and board[row][col] == 0:
        return True
    else:
        return False

def knightTourAlg(board, row, col, step, m, count):

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
        print("\nThis is the m list")
        print(m)
        return True

    print(f"Visiting step {step} at position ({row}, {col})")

    for nextX, nextY in validMoves:
        step[0] += 1
        board[nextX][nextY] = step[0]
        count[0] += 1

        m.append(len(validMoves))

        if knightTourAlg(board, nextX, nextY, step, m, count):
            return True
        
        step[0] -= 1
        board[nextX][nextY] = 0
        m.pop()
    return False

def knightTour(n, posisiX, posisiY):
    
    board = []
    for x in range(0, n):
        row = []
        for y in range(0, n):
            row.append(0)
        board.append(row)

    m = []
    tree_size = [1]
    count = [0]
    step = [1]

    board[posisiX][posisiY] = step[0]

    if knightTourAlg(board, posisiX, posisiY, step, m, count):
        show_result(board, m)
    else:
        show_result([[0]])

    

def est_tree_size(m):
    total = [1]
    product = 1
    for i in m:
        product *= i
        total.append(product)
    return total

# Initializes GUI python
def intro():
    root = tk.Tk()
    root.title("Knight Tour Problem")

    label = tk.Label(root, text="Welcome to knight tour program!")
    label.pack(pady=10)

    # Section for height & width input
    frame1 = tk.Frame(root)
    frame1.pack(padx=10, pady=10)

    label = tk.Label(frame1, text="Enter the width and height for the board :")
    label.pack(side=tk.LEFT)
    ukuran = tk.Entry(frame1)
    ukuran.pack(side=tk.LEFT)

    # Section for X-axis input
    frame2 = tk.Frame(root)
    frame2.pack(padx=10, pady=10)
    
    label = tk.Label(frame2, text="Enter the X-axis of start point : ")
    label.pack(side=tk.LEFT)
    posisiX = tk.Entry(frame2)
    posisiX.pack(side=tk.LEFT)

    # Section for Y-axis input
    frame3 = tk.Frame(root)
    frame3.pack(padx=10, pady=10)

    label = tk.Label(frame3, text="Enter the Y-axis of start point : ")
    label.pack(side=tk.LEFT)
    posisiY = tk.Entry(frame3)
    posisiY.pack(side=tk.LEFT)

    def klik():
        uk_papan = ukuran.get()
        X = int(posisiX.get())
        Y = int(posisiY.get())
        if uk_papan.isdigit() and int(uk_papan) > 0:
            root.destroy()
            knightTour(int(uk_papan), X, Y)
    
    button = tk.Button(root, text="Click to start program", command=klik)
    button.pack(pady=15)

    root.mainloop()

def show_result(board, m):
    n = len(board)
    root = tk.Tk()
    root.title("Knight Tour Result")

    heading = tk.Label(root, text="The board tour result")
    heading.pack(pady=5)

    uk_petak = 60
    canvas = tk.Canvas(root, width=n*uk_petak, height=n*uk_petak)
    canvas.pack()

    for i in range(n):
        for j in range(n):
            x1 = j * uk_petak
            y1 = i * uk_petak
            x2 = x1 + uk_petak
            y2 = y1 + uk_petak

            warna = "white" if (i + j) % 2 == 0 else "gray"
            canvas.create_rectangle(x1, y1, x2, y2, fill=warna)

    totalStep = len(m)+1

    # Search urutan langkah
    step = []
    count = 1
    while count <=totalStep:
        for i in range(n): # As X axis
            for j in range(n): # As Y axis
                if board[i][j] == count:
                    step.append([j,i])
                    count += 1

    for i in range(0, len(step)-1):
        posisi1 = step[i]
        posisi2 = step[i+1]

        X1 = posisi1[0]*uk_petak + uk_petak//2
        Y1 = posisi1[1]*uk_petak + uk_petak//2
        X2 = posisi2[0]*uk_petak + uk_petak//2
        Y2 = posisi2[1]*uk_petak + uk_petak//2
        r = 5

        canvas.create_oval(X1-r, Y1-r, X1+r, Y1+r, fill="red", width=2)
        canvas.create_line(X1 , Y1, X2, Y2, width=4, fill='yellow')
        canvas.create_oval(X2-r, Y2-r, X2+r, Y2+r, fill="red", width=2)
        canvas.after(5)

    size = est_tree_size(m)
    
    frame1 = tk.Frame(root)
    frame1.pack(pady=10)

    mList = tk.Label(frame1, text=f"The M list = {m}")
    mList.pack()

    frame2 = tk.Frame(root)
    frame2.pack(pady=10)

    est_tree = tk.Label(frame2, text=f"The Est. Tree Size = {sum(size):,}")
    est_tree.pack()

    root.mainloop()

if __name__ == "__main__":
    intro()