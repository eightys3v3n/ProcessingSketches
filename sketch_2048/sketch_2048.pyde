import random


TILE_CHANCES_ARRAY = (2, 2, 2, 2, 2, 2, 2, 2, 2, 4) # 10% chance of 4 tile
TILE_COLORS = {0: ((178, 178, 178), (178, 178, 178)),
               2: ((224, 224, 224), (0, 0, 0)),
               4: ((224, 224, 204), (0, 0, 0)),
               8: ((255, 190, 207), (0, 0, 0)),
               16: ((255, 161, 95), (0, 0, 0)),
               32: ((255, 95, 95), (0, 0, 0)),
               64: ((255, 0, 0), (0, 0, 0)),
               128: ((255, 255, 0), (0, 0, 0))}


global gameover
gameover = False
global board
board = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]


def empty_positions():
    global board
    empties = []
    for y, column in enumerate(board):
        for x, val in enumerate(column):
            if val == 0:
                empties.append((x, y))
    return empties


def spawn_tile():
    global gameover
    positions = empty_positions()
    if len(positions) == 0:
        print("Couldn't spawn a new tile")
        gameover = True
        return
    x, y = random.choice(positions)
    val = random.choice(TILE_CHANCES_ARRAY)
    board[y][x] = val 


def move_or_merge_tile(x, y, dx, dy):
    global board
    if dx != 0 and dy != 0:
        raise Exception("Can only move a tile in four directions one at a time")
    if x+dx < 0 or y+dy < 0:
        return False
    elif y+dy >= len(board) or x+dx >= len(board[y]):
        return False
    elif board[y+dy][x+dx] == 0:
        board[y+dy][x+dx] = board[y][x]
        board[y][x] = 0
        return True
    elif board[y+dy][x+dx] == board[y][x]:
        board[y+dy][x+dx] *= 2
        board[y][x] = 0
    return False


def move_board_left():
    global board
    new_tile = False
    for y, column in enumerate(board):
        for x, val in enumerate(column):
            tile_x, tile_y = x, y
            while move_or_merge_tile(tile_x, tile_y, -1, 0):
                tile_x -= 1
                new_tile = True
    return new_tile
                

def move_board_up():
    global board
    new_tile = False
    for y, column in enumerate(board):
        for x, val in enumerate(column):
            tile_x, tile_y = x, y
            while move_or_merge_tile(tile_x, tile_y, 0, -1):
                tile_y -= 1
                new_tile = True
    return new_tile


def move_board_right():
    global board
    new_tile = False
    for y, column in enumerate(board):
        for x in range(len(column)-1, -1, -1):
            tile_x, tile_y = x, y
            while move_or_merge_tile(tile_x, tile_y, 1, 0):
                tile_x += 1
                new_tile = True
    return new_tile


def move_board_down():
    global board
    new_tile = False
    for y in range(len(board)-1, -1, -1):
        for x, val in enumerate(board[y]):
            tile_x, tile_y = x, y
            while move_or_merge_tile(tile_x, tile_y, 0, 1):
                tile_y += 1
                new_tile = True
    return new_tile


def setup():
    size(600, 600)
    global tile_size
    tile_size = (width / 4, height / 4)
    spawn_tile()
    spawn_tile()
    textSize(32)
    textAlign(CENTER, CENTER)
    strokeWeight(3)
    background(240, 240, 240)
    
    
def draw():
    global gameover, tile_size, board
    for y, column in enumerate(board):
        for x, val in enumerate(column):
            tile_color, text_color = TILE_COLORS[val]
            fill(*tile_color)
            stroke(255, 255, 255)
            rect(x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1])
            fill(*text_color)
            noStroke()
            text(val, x * tile_size[0] + tile_size[0] / 2, (y + 1) * tile_size[1] - tile_size[1] / 2)
    
    
def keyPressed():
    global gameover
    if len(empty_positions()) == 0:
        print("no empty positions")
        gameover = True
    if gameover:
        print("Gameover")
        return
    if keyCode == 37:
        if move_board_left():
            spawn_tile()
    elif keyCode == 38:
        if move_board_up():
            spawn_tile()
    elif keyCode == 39:
        if move_board_right():
            spawn_tile()
    elif keyCode == 40:
        if move_board_down():
            spawn_tile()