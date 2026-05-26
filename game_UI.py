import pygame
from board import BoardState 
from move import Move
from SmartMoveFinder import random_AI_moves 

pygame.init()

width = 1024
height = 1024
screen = pygame.display.set_mode((width, height))
square_size = width//8 
rect_surface = pygame.Surface((1024,1024),pygame.SRCALPHA)
rect_surface.fill((0,0,0,192))
dragged_piece = '-'

#Creating a Dictonary for the Pieces to Images
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
promotion_move = None

#Defining King in Check State Variables
black_king_under_check = False
white_king_under_check = False

#for Game Over State
game_is_over = False
game_over_font = pygame.font.SysFont(None, 48) 
winning_string = "" 
winning_rect = pygame.Surface((512,256))
TEXT_COLOR = (255, 255, 255)

#For 3 Moves Repetition Rule
hash_board = dict()

def move_performer(engine_move):
    global is_game_over , winning_string
    initial = engine_move.start_idx
    final = engine_move.end_idx
    piece_to_move = Board.board[initial]
    captured = Board.board[final]

    if(engine_move.is_castled==True):
        #Performing Black King's Queen Side Castling if Conditions are correct
        if(piece_to_move=='k' and final == 23 and initial == 25 and Board.black_queen_side_castle==True):
            Board.board[23]='k'
            Board.board[25]='-'
            Board.board[24]='r'
            Board.board[21]='-'
            Board.r1move=True
            Board.black_king_move=True
            Board.counter+=1
            Board.half_move_counter += 1

        #Performing Black King's King Side Castling if Conditions are correct
        elif(piece_to_move=='k' and final == 27 and initial == 25 and Board.black_king_side_castle==True):
            Board.board[27]='k'
            Board.board[25]='-'
            Board.board[28]='-'
            Board.board[26]='r'
            Board.r2move=True
            Board.black_king_move=True
            Board.counter+=1
            Board.half_move_counter += 1

        #Performing White King's Queen Side Castling if Conditions are correct
        elif(piece_to_move=='K' and final == 93 and initial == 95 and Board.white_queen_side_castle==True):
            Board.board[93]='K'
            Board.board[95]='-'
            Board.board[94]='R'
            Board.board[91]='-'
            Board.R1move=True
            Board.white_king_move=True
            Board.counter+=1
            Board.half_move_counter += 1

        #Performing White King's King Side Castling if Conditions are correct
        elif(piece_to_move=='K' and final == 97 and initial == 95 and Board.white_king_side_castle==True):
            Board.board[97]='K'
            Board.board[95]='-'
            Board.board[98]='-'
            Board.board[96]='R'
            Board.R2move=True
            Board.white_king_move=True
            Board.counter+=1
            Board.half_move_counter += 1
    
    #Pawn Promotion For Human
    elif(engine_move.is_promotion==True and engine_move.pawn_promoted_to=='-'):
        #Check for the pawn promotion move (as it's move_ID is different)
        if (piece_to_move == 'P' and final // 10 == 2) or (piece_to_move == 'p' and final // 10 == 9):
            global is_pawn_promotion 
            global promotion_move 
            is_pawn_promotion = True
            promotion_move = engine_move
            promotion_move.is_promotion = True
            return

    #Pawn Promotion For AI
    elif(engine_move.is_promotion==True and engine_move.pawn_promoted_to!='-'):
        Board.board[final]=engine_move.pawn_promoted_to
        Board.board[initial]='-'
        Board.counter+=1
        Board.half_move_counter = 0 
            
    elif(engine_move.is_en_passant==True):
        #EnPassant Move
        if piece_to_move == 'P':
            Board.board[final + 10] = '-' 
            Board.board[final] = 'P'
            
        elif piece_to_move == 'p':
            Board.board[final - 10] = '-'
            Board.board[final]='p'

        Board.board[initial] = '-'
        Board.counter+=1
        Board.half_move_counter = 0 

    else:
        Board.board[final]=piece_to_move
        Board.board[initial]='-'  
        Board.counter+=1
        if(piece_to_move=='p' or piece_to_move=='P' or captured!='-'):
            Board.half_move_counter = 0 
        else:
            Board.half_move_counter += 1 

        #For EnPaussant Changes
        Board.en_passant_target = -1
        if (piece_to_move == 'P' and initial - final == 20):
            Board.en_passant_target = final + 10
        elif (piece_to_move == 'p' and final - initial == 20):
            Board.en_passant_target = final - 10
        #For Castling Changes
        elif(piece_to_move == 'r' and initial == 21 and Board.r1move==False):
            Board.r1move=True
        elif(piece_to_move == 'r' and initial == 28 and Board.r2move==False):
            Board.r2move=True
        elif(piece_to_move == 'R' and initial == 91 and Board.R1move==False):
            Board.R1move=True
        elif(piece_to_move == 'R' and initial == 98 and Board.R2move==False):
            Board.R2move=True
        elif(piece_to_move =='k' and initial == 25 and Board.black_king_move==False):
            Board.black_king_move=True
        elif(piece_to_move =='K' and initial == 95 and Board.white_king_move==False):
            Board.white_king_move=True

    #For 3 Move Repetation Rule
    board_string = Board.board_to_string()
    board_string+=str(Board.counter%2)
    hash_board[board_string] = hash_board.get(board_string, 0) + 1
    if(hash_board[board_string]==3):
        game_is_over = True
        winning_string = "Draw by 3-Move Repetation Rule"

    #For 50 Move Rule 
    if(piece_to_move=='p' or piece_to_move == 'P' or captured!='-'):
        Board.half_move_counter=0
    if(Board.half_move_counter==100):
        game_is_over=True
        winning_string = "Draw by 50-Move Rule"

    is_game_over()

def is_game_over():
    global list_of_legal_moves , winning_string , game_is_over
    list_of_legal_moves = []
    global white_king_under_check , black_king_under_check
    #For Checking if Game Is Over 
    if(Board.counter%2==0):
        #Checking if the White King is in Check or not
        if(Board.white_king_in_check()==True):
            white_king_under_check = True
        else:
            white_king_under_check = False

        #Checking if the Black King is in Check or not
        if(Board.black_king_in_check()==True):
            black_king_under_check = True
        else:
            black_king_under_check = False

        there_are_legal_moves = False
        for i in range(120):
            if(Board.board[i].isupper()==True):
                x = (i % 10) - 1
                y = (i - 20) // 10
                list_of_legal_moves += Board.legal_moves(Board.board[i],x,y)
        if(len(list_of_legal_moves) >0 ):
            there_are_legal_moves = True
                    
        if(there_are_legal_moves == False):
            game_is_over = True
            if(Board.white_king_in_check() == True):
                winning_string = "Black Wins"
            elif(Board.white_king_in_check() == False):
                winning_string = "Stalemate"

    if(Board.counter%2==1):
        #Checking if the Black King is in Check or not
        if(Board.black_king_in_check()==True):
            black_king_under_check = True
        else:
            black_king_under_check = False

        #Checking if the White King is in Check or not
        if(Board.white_king_in_check()==True):
            white_king_under_check = True
        else:
            white_king_under_check = False

        there_are_legal_moves = False
        for i in range(120):
            if(Board.board[i].islower()==True and Board.board[i]!='x'):
                x = (i % 10) - 1
                y = (i - 20) // 10
                list_of_legal_moves += Board.legal_moves(Board.board[i],x,y)
        if(len(list_of_legal_moves) >0 ):
            there_are_legal_moves = True
                   
        if(there_are_legal_moves == False):
            game_is_over = True
            if(Board.black_king_in_check() == True):
                winning_string = "White Wins"
            elif(Board.black_king_in_check() == False):
                winning_string = "stalemate"


def square_coloring(init_x,init_y):
    pygame.draw.circle(screen,(176,224,230),(init_x*square_size+64,init_y*square_size+64),56)
    index = init_y*10 + 20 + init_x + 1
    if(dragged_piece=='k' and Board.black_king_side_castle==True and index==25):
        pygame.draw.circle(screen,(255,255,224),(6*square_size+64,64),56)
    if(dragged_piece=='k' and Board.black_queen_side_castle==True and index==25):
        pygame.draw.circle(screen,(255,255,224),(2*square_size+64,64),56)
    if(dragged_piece=='K' and Board.white_king_side_castle==True and index ==95):
        pygame.draw.circle(screen,(255,255,224),(6*square_size+64,7*square_size+64),56)
    if(dragged_piece=='K' and Board.white_queen_side_castle==True and index ==95):
        pygame.draw.circle(screen,(255,255,224),(2*square_size+64,7*square_size+64),56)
    for i in range(len(current_legal_moves)):
        index = current_legal_moves[i].end_idx
        x = index%10 - 1 
        y = (index-20)//10
        pygame.draw.circle(screen,(255,255,224),(x*square_size+64,y*square_size+64),56)
    

def coloring_check():
    rectangle = pygame.Surface((square_size,square_size))
    rectangle.fill((255,204,203))
    if(black_king_under_check==True):
        index = - 1
        for i in range(120):
            if(Board.board[i]=='k'):
                index = i 
                break
        x = index%10 - 1 
        y = (index-20)//10
        screen.blit(rectangle,(x*square_size,y*square_size))
    elif(white_king_under_check==True):
        index = - 1
        for i in range(120):
            if(Board.board[i]=='K'):
                index = i 
                break
        x = index%10 - 1 
        y = (index-20)//10
        screen.blit(rectangle,(x*square_size,y*square_size))

playerOne = True #Player One is white and True means Human else AI
playerTwo = False #Player Two is Black and True means Human else AI
 
running = True
while running : 
    for event in pygame.event.get():

        is_human_move = ((playerOne==True and Board.counter%2==0) or (playerTwo==True and Board.counter%2==1))

        if(event.type == pygame.QUIT):
            running = False

        elif (is_pawn_promotion==True and event.type == pygame.MOUSEBUTTONDOWN and is_human_move):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            piece_to_move = Board.board[promotion_move.start_idx]
            chosen_piece = '\0'
            if(448 <= mouse_y <= 448 + square_size):
                if(256 <= mouse_x < 384):
                    chosen_piece = 'q' if piece_to_move.islower() else 'Q'
                elif(384 <= mouse_x < 512):
                    chosen_piece = 'r' if piece_to_move.islower() else 'R'
                elif(512 <= mouse_x < 640):
                    chosen_piece = 'b' if piece_to_move.islower() else 'B'
                elif(640 <= mouse_x < 768):
                    chosen_piece = 'n' if piece_to_move.islower() else 'N'
            if chosen_piece != '\0':
                # Rebuild move_id with chosen promotion letter
                promotion_move.pawn_promoted_to = chosen_piece
                promotion_move.move_id +=  chosen_piece
                if promotion_move in current_legal_moves:
                    Board.board[promotion_move.end_idx] = chosen_piece
                    Board.board[promotion_move.start_idx] = '-'
                    is_pawn_promotion = False
                    promotion_move = None
                    Board.counter += 1
                    Board.half_move_counter = 0
                    is_game_over()

        #when we pick up a piece from a square
        elif (game_is_over==False and dragging==False and event.type == pygame.MOUSEBUTTONDOWN and is_human_move):
            mouse_x,mouse_y=pygame.mouse.get_pos()
            drag_x,drag_y=mouse_x,mouse_y
            mouse_x = mouse_x//square_size
            mouse_y = mouse_y//square_size
            initial_index = mouse_y*10+20 + mouse_x + 1
            if(Board.board[initial_index]!='x' and Board.board[initial_index]!='-'):
                dragged_piece = Board.board[initial_index]

                is_valid_turn = True
                if(Board.counter%2==0 and dragged_piece.islower()):
                    is_valid_turn = False
                elif(Board.counter%2==1 and dragged_piece.isupper()):
                    is_valid_turn = False

                if (is_valid_turn == True):
                    current_legal_moves = Board.legal_moves(dragged_piece,mouse_x,mouse_y)
                    Board.board[initial_index]='-'
                    dragging = True
                else:
                    Board.board[initial_index]=dragged_piece
        
        #when we are dargging the piece
        elif (game_is_over == False and dragging==True and event.type == pygame.MOUSEMOTION and is_human_move):
            drag_x,drag_y = pygame.mouse.get_pos()

        #When we put the piece in a square
        elif (game_is_over==False and dragging==True and event.type ==pygame.MOUSEBUTTONUP and is_human_move):
            mouse_x,mouse_y = pygame.mouse.get_pos()
            mouse_x = mouse_x//square_size
            mouse_y = mouse_y//square_size
            final_index = mouse_y*10+20 + mouse_x + 1

            is_promoting = ( (dragged_piece == 'P' and mouse_y == 0) or (dragged_piece == 'p' and mouse_y == 7) )
            if is_promoting:
                matched = None
                for m in current_legal_moves:
                    if m.is_promotion and m.start_idx == initial_index and m.end_idx == final_index:
                        matched = m
                        break
                if matched is not None:
                    is_pawn_promotion = True
                    promotion_move = matched
            #putting the piece back to the original place to generate move_id correctly
            Board.board[initial_index] = dragged_piece
            if(Board.board[final_index]!='x'):
                attempted_move = Move(initial_index,final_index,Board.board)  

            if(attempted_move in current_legal_moves):
                list_idx = current_legal_moves.index(attempted_move)
                engine_move = current_legal_moves[list_idx]
                move_performer(engine_move)
                                
            dragging = False 

        elif(game_is_over==False and not is_human_move):
            ai_idx = random_AI_moves(list_of_legal_moves)
            if(ai_idx == -1):
                game_is_over=True
            else :    
                move_performer(list_of_legal_moves[ai_idx])

    for x in range (8):
        for y in range (8) :
            x_coordinate = x * square_size
            y_coordinate = y * square_size
            rect = pygame.Surface((square_size,square_size))
            if((x+y)%2==0):
                rect.fill((255,255,255))
            else:
                rect.fill((170,170,170))
            screen.blit(rect,(x_coordinate,y_coordinate))

    if(dragging == True):
        square_coloring(mouse_x,mouse_y)

    if(black_king_under_check == True or white_king_under_check == True):
        coloring_check()

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
        if(promotion_move.piece_moved.isupper()):
            promotion_list = ['Q','R','B','N']
        elif(promotion_move.piece_moved.islower()):
            promotion_list = ['q','r','b','n']
        screen.blit(rect_surface,(0,0))
        for i in range(4):
            screen.blit(pieces[promotion_list[i]],(256+128*i,448))
            
    if(game_is_over==True):
        screen.blit(rect_surface,(0,0))
        screen.blit(winning_rect,(256,384))
        text_surface = game_over_font.render(winning_string, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        win_box_bounds = winning_rect.get_rect(topleft=(256,384))
        text_rect.center = win_box_bounds.center
        screen.blit(text_surface, text_rect)

    if dragging :
        offset = square_size // 2 
        screen.blit(pieces[dragged_piece],(drag_x-offset,drag_y-offset))

    pygame.display.flip()

pygame.quit()