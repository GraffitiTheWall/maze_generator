import random
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, green, red

WIDTH = 51
HEIGHT = 51
board = [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]
stack = []


def is_valid(x, y):
    return 0 <= x < WIDTH and 0 <= y < HEIGHT


def carve_canvas(x, y):
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
            stack.append((new_cell_x, new_cell_y))
            carve_canvas(new_cell_x, new_cell_y)


start_x, start_y = (1, 1)
carve_canvas(start_x, start_y)

board[1][1] = "S"
end_x, end_y = max(stack)
board[end_y][end_x] = "E"

w = WIDTH * 15
h = HEIGHT * 15
c = canvas.Canvas("maze.pdf", pagesize=(w, h))
c.setFillColor(black)
x, y = 0, h - 15

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
