import pygame
#linking board.py with game_UI.py
from board import BoardState 
from move import Move

pygame.init()

width = 1024
height = 1024
screen = pygame.display.set_mode((width, height))
square_size = width//8 
background = pygame.image.load('Chess_images/rect-8x8.svg').convert_alpha()
background = pygame.transform.scale(background,(width,height))
rect_surface = pygame.Surface((1024,1024),pygame.SRCALPHA)
rect_surface.fill((0,0,0,192))
counter = 0 

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

#mouse logic starts here
dragging = False
dragged_piece = '\0'
initial_index = -1
final_index = -1
drag_x = -1
drag_y = -1
mouse_x = -1
mouse_y = -1
current_legal_moves = []
is_pawn_promotion = False
promotion_move = Move

running = True
while running : 
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        
        #Resuming the game
        elif(is_pawn_promotion==True and event.type == pygame.MOUSEBUTTONDOWN):
            mouse_x,mouse_y = pygame.mouse.get_pos()
            chosen_piece='\0'
            if(448<=mouse_y<=448+square_size):
                if(256<=mouse_x<384):
                    if(dragged_piece.islower()):
                        chosen_piece='q'
                    else:
                        chosen_piece='Q'
                elif(384<=mouse_x<512):
                    if(dragged_piece.islower()):
                        chosen_piece='r'
                    else:
                        chosen_piece='R'
                elif(512<=mouse_x<640):
                    if(dragged_piece.islower()):
                        chosen_piece='b'
                    else:
                        chosen_piece='B'
                elif(640<=mouse_x<768):
                    if(dragged_piece.islower()):
                        chosen_piece='n'
                    else:
                        chosen_piece='N'
            promotion_move.move_id += chosen_piece
            if(promotion_move in current_legal_moves):

                list_idx = current_legal_moves.index(promotion_move)
                engine_move = current_legal_moves[list_idx]

                Board.board[promotion_move.end_idx] = chosen_piece
                Board.board[promotion_move.start_idx] = '-' 
                is_pawn_promotion = False
                counter+=1

        #when we pick up a piece from a square
        elif (dragging==False and event.type == pygame.MOUSEBUTTONDOWN):
            mouse_x,mouse_y=pygame.mouse.get_pos()
            drag_x,drag_y=mouse_x,mouse_y
            mouse_x = mouse_x//square_size
            mouse_y = mouse_y//square_size
            initial_index = mouse_y*10+20 + mouse_x + 1
            if(Board.board[initial_index]!='x' and Board.board[initial_index]!='-'):
                dragged_piece = Board.board[initial_index]

                is_valid_turn = True
                if(counter%2==0 and dragged_piece.islower()):
                    is_valid_turn = False
                elif(counter%2==1 and dragged_piece.isupper()):
                    is_valid_turn = False

                if (is_valid_turn == True):
                    current_legal_moves = Board.legal_moves(dragged_piece,mouse_x,mouse_y)
                    Board.board[initial_index]='-'
                    dragging = True
                else:
                    Board.board[initial_index]=dragged_piece
        
        #when we are dargging the piece
        elif (dragging==True and event.type == pygame.MOUSEMOTION):
            drag_x,drag_y = pygame.mouse.get_pos()

        #When we put the piece in a square
        elif (dragging==True and event.type ==pygame.MOUSEBUTTONUP):
            mouse_x,mouse_y = pygame.mouse.get_pos()
            mouse_x = mouse_x//square_size
            mouse_y = mouse_y//square_size
            final_index = mouse_y*10+20 + mouse_x + 1

            #putting the piece back to the original place to generate move_id correctly
            Board.board[initial_index] = dragged_piece
            if(Board.board[final_index]!='x'):
                attempted_move = Move(initial_index,final_index,Board.board)
                
                #Check for the pawn promotion move (as it's move_ID is different)
                if (dragged_piece == 'P' and final_index // 10 == 2) or (dragged_piece == 'p' and final_index // 10 == 9):
                    is_pawn_promotion = True
                    promotion_move = attempted_move
                    promotion_move.is_promotion = True
                    #Pausing the game

                else:
                    if(attempted_move in current_legal_moves):

                        list_idx = current_legal_moves.index(attempted_move)
                        engine_move = current_legal_moves[list_idx]

                        Board.board[final_index] = dragged_piece
                        Board.board[initial_index] = '-' 

                        #trying for enPassant
                        if engine_move.is_en_passant == True:
                            if dragged_piece == 'P':
                                Board.board[final_index + 10] = '-' 
                            elif dragged_piece == 'p':
                                Board.board[final_index - 10] = '-'

                        Board.en_passant_target = -1
                        if (dragged_piece == 'P' and initial_index - final_index == 20):
                            Board.en_passant_target = final_index + 10
                        elif (dragged_piece == 'p' and final_index - initial_index == 20):
                            Board.en_passant_target = final_index - 10
                        counter+=1

            dragging = False 


    screen.blit(background,(0,0))
    for i in range(120):
        if(Board.board[i]=='x'):
            continue
        elif(Board.board[i]!='-'):
            piece_to_draw = pieces[Board.board[i]]
            x_pos = ((i%10)-1)*square_size
            y_pos = ((i-20)//10)* square_size
            screen.blit(piece_to_draw,(x_pos,y_pos))

    if(is_pawn_promotion):
        promotion_list = []
        if(dragged_piece.isupper()):
            promotion_list = ['Q','R','B','N']
        elif(dragged_piece.islower()):
            promotion_list = ['q','r','b','n']
        screen.blit(rect_surface,(0,0))
        for i in range(4):
            screen.blit(pieces[promotion_list[i]],(256+128*i,448))
            

    if dragging :
        offset = square_size // 2 
        screen.blit(pieces[dragged_piece],(drag_x-offset,drag_y-offset))

    pygame.display.flip()

pygame.quit()