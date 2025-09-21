import random
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, green, red

#Defines the WIDTH and the HEIGHT of the board. You may change them, but, THEY MUST BE ODD NUMBERS!
WIDTH = 51
HEIGHT = 51

#A cell with the value of 1 is filled in (a wall), whereas, a cell with the value of 0 is empty (no wall).
board = [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]

#The 'stack' list is used to store in the empty cells in the board.
stack = []


def is_valid(x, y):
    '''
    Checks if the x and the y coordinates are in the bounds of the board.
    '''
    return 0 <= x < WIDTH and 0 <= y < HEIGHT


def carve_canvas(x, y):
    '''
    This carves out the board in the array. It basically picks out a new cell adjacent to the current cell, and, if the x and y coordinates
    are valid points and the new cell hasn't already been carved out by another cell, it removes the wall between them (1 for wall, 0 for
    no wall) and recurses to the next cell (i.e., the new cell).
    '''
    board[y][x] = 0
    dirrs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    random.shuffle(dirrs)
    for nx, ny in dirrs:
        new_cell_x, new_cell_y = nx + x, ny + y
        wall_x, wall_y = x + nx // 2, y + ny // 2
        if (
            is_valid(new_cell_x, new_cell_y) == True
            and board[new_cell_y][new_cell_x] == 1
        ):
            board[wall_y][wall_x] = 0
            #We append each cell to the 'stack' list, so that we can figure out which cell is the furthest away from the starting point, 
            #(1 , 1).
            stack.append((new_cell_x, new_cell_y))
            carve_canvas(new_cell_x, new_cell_y)


start_x, start_y = (1, 1)
carve_canvas(start_x, start_y)

board[1][1] = "S"
#We find the end of the maze by choosing the furthest empty cell from the starting cell, using 'max(stack)'.
end_x, end_y = max(stack)
board[end_y][end_x] = "E"

w = WIDTH * 15
h = HEIGHT * 15
c = canvas.Canvas("maze.pdf", pagesize=(w, h))
c.setFillColor(black)
x, y = 0, h - 15

#This program then proceeds to carving out the board into the reportlab canvas pdf file. It outputs it as 'maze.pdf' for the user to use. The
#start will be colored in with a green square, whereas the end will be colors in with a red square. A cell with the value of 1 (meaning that
#there is a wall) will be black, and white if it has the value of 0 (meaning that there is no wall, and, that the cell is empty).
for row in board:
    for i in range(len(row)):
        if row[i] == 1:
            c.rect(x, y, 15, 15, fill=1)
        elif row[i] == 0:
            c.rect(x, y, 15, 15)
        elif row[i] == "S":
            c.setFillColor(green)
            c.rect(x, y, 15, 15, fill=1)
            c.setFillColor(black)
        elif row[i] == "E":
            c.setFillColor(red)
            c.rect(x, y, 15, 15, fill=1)
            c.setFillColor(black)
        x += 15
    x = 0
    y -= 15
c.save()
