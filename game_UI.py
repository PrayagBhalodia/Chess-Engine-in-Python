import pygame
#linking board.py with game_UI.py
from board import BoardState 


pygame.init()

width = 1024
height = 1024
screen = pygame.display.set_mode((width, height))
square_size = width/8 
background = pygame.image.load('Chess_images/rect-8x8.svg').convert_alpha()
background = pygame.transform.scale(background,(width,height))

#creating a dictonary for the pieces to images
pieces={
    'R' : pygame.image.load('Chess_images/rook-w.svg').convert_alpha(),
    'r' : pygame.image.load('Chess_images/rook-b.svg').convert_alpha(),
    'N' : pygame.image.load('Chess_images/knight-w.svg').convert_alpha(),
    'n' : pygame.image.load('Chess_images/knight-b.svg').convert_alpha(),
    'B' : pygame.image.load('Chess_images/bishop-w.svg').convert_alpha(),
    'b' : pygame.image.load('Chess_images/bishop-b.svg').convert_alpha(),
    'P' : pygame.image.load('Chess_images/pawn-w.svg').convert_alpha(),
    'p' : pygame.image.load('Chess_images/pawn-b.svg').convert_alpha(),
    'q' : pygame.image.load('Chess_images/queen-b.svg').convert_alpha(),
    'Q' : pygame.image.load('Chess_images/queen-w.svg').convert_alpha(),
    'K' : pygame.image.load('Chess_images/king-w.svg').convert_alpha(),
    'k' : pygame.image.load('Chess_images/king-b.svg').convert_alpha(),
}

Board = BoardState()

running = True
while running : 
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False

    screen.blit(background,(0,0))
    for i in range(120):
        if(Board.board[i]=='x'):
            continue
        elif(Board.board[i]!='-'):
            piece_to_draw = pieces[Board.board[i]]
            x_pos = ((i%10)-1)*square_size
            y_pos = ((i-20)//10)* square_size
            screen.blit(piece_to_draw,(x_pos,y_pos))

    pygame.display.flip()

pygame.quit()