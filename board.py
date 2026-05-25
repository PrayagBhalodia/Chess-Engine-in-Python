from move import Move

class BoardState :
    def __init__ (self):
        #For EnPassant Move
        self.en_passant_target = -1

        #For Castle Move
        self.r1move = False
        self.r2move = False
        self.R1move = False
        self.R2move = False
        self.black_king_move = False
        self.white_king_move = False
        self.black_king_side_castle = False
        self.white_king_side_castle = False
        self.black_queen_side_castle = False
        self.white_queen_side_castle = False


        self.board = [
                 'x','x','x','x','x','x','x','x','x','x',
                 'x','x','x','x','x','x','x','x','x','x',
                 'x','r','n','b','q','k','b','n','r','x',
                 'x','p','p','p','p','p','p','p','p','x',
                 'x','-','-','-','-','-','-','-','-','x',
                 'x','-','-','-','-','-','-','-','-','x',
                 'x','-','-','-','-','-','-','-','-','x',
                 'x','-','-','-','-','-','-','-','-','x',
                 'x','P','P','P','P','P','P','P','P','x',
                 'x','R','N','B','Q','K','B','N','R','x',
                 'x','x','x','x','x','x','x','x','x','x',
                 'x','x','x','x','x','x','x','x','x','x',
                 ]
        self.counter = 0 
        self.half_move_counter = 0
        self.game_history = []
        self.history_pointer = 0
        self.save_state()

#------------------------------------------FUNCTION TO SAVE THE THE HISTORY FOR UNDO/REDO-----------------------------------------------------
    def save_state(self):
        current_state = {
            "board" : self.board.copy(),
            "ep_target" : self.en_passant_target,
            "castling" : [
                self.r1move , self.r2move , self.R1move , self.R2move , 
                self.black_king_move , self.white_king_move ,
                self.black_king_side_castle, self.white_king_side_castle,
                self.black_queen_side_castle, self.white_queen_side_castle
            ],
            "half_moves": self.half_move_counter,
            "turn_counter": self.counter
        }
        self.game_history = self.game_history[:self.history_pointer + 1]
        self.game_history.append(current_state)
        self.history_pointer += 1

    def load_state(self):
        state = self.game_history[self.history_pointer]
        self.board = state["board"].copy()
        self.en_passant_target = state["ep_target"]
        
        flags = state["castling"]
        self.r1move, self.r2move, self.R1move, self.R2move = flags[0], flags[1], flags[2], flags[3]
        self.black_king_move, self.white_king_move = flags[4], flags[5]
        self.black_king_side_castle, self.white_king_side_castle = flags[6], flags[7]
        self.black_queen_side_castle, self.white_queen_side_castle = flags[8], flags[9]
        
        self.half_move_counter = state["half_moves"]
        self.counter = state["turn_counter"]

#--------------------------------------------------BOARD TO STRING HELPER FUNCTION -------------------------------------------------------------
    def board_to_string(self):
        board_string = ""
        for i in range (120):
            if(self.board[i]!='x'):
                if(self.board[i]=='-'):
                    board_string+="0"
                else:
                    board_string+=self.board[i]
        board_string+=str(self.en_passant_target)+str(self.white_king_side_castle)+str(self.black_king_side_castle)+str(self.black_queen_side_castle)+str(self.white_queen_side_castle)
        return board_string

#---------------------------------------------------HELPER FUNCTIONS FOR PSEUDO LEGAL MOVES---------------------------------------------

    def ray_helper_function(self,piece,direction , x , y):
        moves_list = []
        index = y*10+20+x+1

        step_map = {
            "up": -10, "down": 10, "left": -1, "right": 1,
            "diag1": -11, "diag2": -9, "diag3": 9, "diag4": 11
        }
        step = step_map[direction]

        while True:
            index += step
            target = self.board[index]
            if(target=='-'):
                moves_list.append(index)
            elif(target=='x'):
                return moves_list
            else:
                break

        if(self.is_enemy(piece,index)):
            moves_list.append(index)

        return moves_list

    def is_enemy(self,piece,index):
        #White Piece
        if(piece.isupper()):
            if(self.board[index].islower() and self.board[index]!='x'):
                return True

        #Black Piece
        if(piece.islower()):
            if(self.board[index].isupper() ):
                return True
                
        return False

#---------------------------------------------------GENERATING PSEUDO LEGAL MOVES-------------------------------------------------------
 
    def pseudo_legal_moves(self,piece, init_x , init_y):
        moves =[]
        index = 10*init_y+20+init_x+1

        #FOR QUEEN PSEUDO LEGAL MOVES
        if(piece=='Q' or piece=='q'):
            moves += ( self.ray_helper_function(piece,"diag1",init_x,init_y) + self.ray_helper_function(piece,"diag2",init_x,init_y) 
                    + self.ray_helper_function(piece,"diag3",init_x,init_y) + self.ray_helper_function(piece,"diag4",init_x,init_y)
                    + self.ray_helper_function(piece,"up",init_x,init_y) + self.ray_helper_function(piece,"left",init_x,init_y)
                    + self.ray_helper_function(piece,"down",init_x,init_y) + self.ray_helper_function(piece,"right",init_x,init_y)
            )

        #FOR ROOK PSEUDO LEGAL MOVES
        elif(piece=='R' or piece=='r'):
            moves += (self.ray_helper_function(piece,"up",init_x,init_y) + self.ray_helper_function(piece,"left",init_x,init_y)
                    + self.ray_helper_function(piece,"down",init_x,init_y) + self.ray_helper_function(piece,"right",init_x,init_y)
            )

        #FOR BISHOP PSEUDO LEGAL MOVES
        elif(piece=='b' or piece =='B'):
            moves += ( self.ray_helper_function(piece,"diag1",init_x,init_y) + self.ray_helper_function(piece,"diag2",init_x,init_y) 
                    + self.ray_helper_function(piece,"diag3",init_x,init_y) + self.ray_helper_function(piece,"diag4",init_x,init_y)
            )

        #FOR KNIGHT PSEUDO LEGAL MOVES
        elif(piece=='n' or piece =='N'):
            if(self.board[index-21]!='x' and (self.board[index-21]=='-' or self.is_enemy(piece,index-21))):
                moves.append(index-21)
            if(self.board[index+21]!='x' and (self.board[index+21]=='-' or self.is_enemy(piece,index+21))):
                moves.append(index+21)
            if(self.board[index-12]!='x' and (self.board[index-12]=='-' or self.is_enemy(piece,index-12))):
                moves.append(index-12)
            if(self.board[index+12]!='x' and (self.board[index+12]=='-' or self.is_enemy(piece,index+12))):
                moves.append(index+12)  
            if(self.board[index-19]!='x' and (self.board[index-19]=='-' or self.is_enemy(piece,index-19))):
                moves.append(index-19)
            if(self.board[index+19]!='x' and (self.board[index+19]=='-' or self.is_enemy(piece,index+19))):
                moves.append(index+19)    
            if(self.board[index-8]!='x' and (self.board[index-8]=='-' or self.is_enemy(piece,index-8))):
                moves.append(index-8) 
            if(self.board[index+8]!='x' and (self.board[index+8]=='-' or self.is_enemy(piece,index+8))):
                moves.append(index+8) 

        #FOR KING PSEUDO LEGAL MOVES
        elif(piece=='k' or piece=='K'):
            if(self.board[index-1]!='x' and (self.board[index-1]=='-' or self.is_enemy(piece,index-1))):
                moves.append(index-1)
            if(self.board[index+1]!='x'and (self.board[index+1]=='-' or self.is_enemy(piece,index+1))):
                moves.append(index+1)
            if(self.board[index-10]!='x' and (self.board[index-10]=='-' or self.is_enemy(piece,index-10))):
                moves.append(index-10)
            if(self.board[index+10]!='x' and (self.board[index+10]=='-' or self.is_enemy(piece,index+10))):
                moves.append(index+10)
            if(self.board[index-11]!='x' and (self.board[index-11]=='-' or self.is_enemy(piece,index-11))):
                moves.append(index-11)
            if(self.board[index+11]!='x' and (self.board[index+11]=='-' or self.is_enemy(piece,index+11))):
                moves.append(index+11)
            if(self.board[index-9]!='x' and (self.board[index-9]=='-' or self.is_enemy(piece,index-9))):
                moves.append(index-9)
            if(self.board[index+9]!='x' and (self.board[index+9]=='-' or self.is_enemy(piece,index+9))):
                moves.append(index+9)
            
        #FOR BLACK PAWN PSEUDO LEGAL MOVES
        elif(piece=='p'):
            #Attack White Peices by Black Pawn moves
            if (self.board[index+11]!='-' and self.board[index+11]!='x' and self.board[index+11].isupper() ):
                moves.append(index+11)
            if (self.board[index+9]!='-' and self.board[index+9]!='x' and self.board[index+9].isupper()):
                moves.append(index+9)

            if(init_y==1):
                if(self.board[index+10]=='-'):
                    moves.append(index+10)
                    if(self.board[index+20]=='-'):
                        moves.append(index+20)

            elif(init_y<=6):
                #enPaussant check
                if(init_y==4):
                    if (self.board[index+11]=='-' and self.en_passant_target == index+11 ):
                        moves.append(index+11)
                    if (self.board[index+9]=='-' and self.en_passant_target == index+9):
                        moves.append(index+9)

                if(self.board[index+10]=='-'):
                    moves.append(index+10)

        #FOR WHITE PAWN PSEUDO LEGAL MOVES
        elif(piece=='P'):
            #Attack Black Peices by White Pawn moves
            if (self.board[index-11]!='-' and self.board[index-11]!='x' and self.board[index-11].islower() ):
                moves.append(index-11)
            if (self.board[index-9]!='-' and self.board[index-9]!='x' and self.board[index-9].islower()):
                moves.append(index-9)

            if(init_y==6):
                if(self.board[index-10]=='-'):
                    moves.append(index-10)
                    if(self.board[index-20]=='-'):
                        moves.append(index-20)

            elif(init_y>=1):
                #enPaussant check
                if(init_y==3):
                    if (self.board[index-11]=='-' and self.en_passant_target == index-11):
                        moves.append(index-11)
                    if (self.board[index-9]=='-' and self.en_passant_target == index-9):
                        moves.append(index-9)

                if(self.board[index-10]=='-'):
                    moves.append(index-10)

        return moves

#-------------------------------------------CHECKER FUNCTION TO CHECK FOR CHECK-----------------------------------------------------------

    def white_king_in_check(self):
        index = -1
        for i in range(120):
            if(self.board[i]=='K'):
                index = i 
                break
        king = self.board[i]
    
        #Queen , Rook , Bishop check logic
        step_moves = [1,9,10,11,-1,-9,-10,-11]
        for i in range(8):
            step = step_moves[i]
            pointer = index+step
            while(self.board[pointer]!='x'):
                if(self.is_enemy(king,pointer)==False):
                    if(self.board[pointer].isupper()):
                        break
                    pointer+=step
                else:
                    if(self.board[pointer]=='q'):
                        return True
                    elif(self.board[pointer]=='r' and (step==-10 or step==-1 or step==1 or step==10)):
                        return True
                    elif(self.board[pointer]=='b' and (step==-11 or step==-9 or step==9 or step==11)):
                        return True
                    break

        #Knight check logic
        knight_moves = [-21,-19,-12,-8,8,12,19,21]
        for i in range(8):
            if(self.board[index+knight_moves[i]]=='n'):
                return True

        #Pawn check logic
        if(self.board[index-11]=='p' or self.board[index-9]=='p'):
            return True
            
        return False

    def black_king_in_check(self):
        index = -1
        for i in range(120):
            if(self.board[i]=='k'):
                index = i 
                break
        king = self.board[i]

        #Queen , Rook , Bishop check logic
        step_moves = [1,9,10,11,-1,-9,-10,-11]
        for i in range(8):
            step = step_moves[i]
            pointer = index+step
            while(self.board[pointer]!='x'):
                if(self.is_enemy(king,pointer)==False):
                    if(self.board[pointer].islower()):
                        break
                    pointer+=step
                else:   
                    if(self.board[pointer]=='Q'):
                        return True
                    elif(self.board[pointer]=='R' and (step==-10 or step==-1 or step==1 or step==10)):
                        return True
                    elif(self.board[pointer]=='B' and (step==-11 or step==-9 or step==9 or step==11)):
                        return True
                    break

        #Knight check logic
        knight_moves = [-21,-19,-12,-8,8,12,19,21]
        for i in range(8):
            if(self.board[index+knight_moves[i]]=='N'):
                return True

        #Pawn check logic
        if(self.board[index+11]=='P' or self.board[index+9]=='P'):
            return True
            
        return False

#-----------------------------------------------LEGAL MOVES GENERATOR---------------------------------------------------------------

    def legal_moves (self,piece,init_x,init_y):
        index = 10*init_y+20 + init_x + 1
        pseudo = self.pseudo_legal_moves(piece,init_x,init_y)

        piece_color = ""
        if(piece.isupper()):
            piece_color = "White"
        elif(piece.islower()):
            piece_color="Black"
        
        legal_moves = []

        #Check for Black King's Queen Side Castle
        if(piece=='k' and self.r1move == False and self.black_king_move == False and 
           self.board[22]=='-' and self.board[23]=='-' and self.board[24]=='-' and self.black_king_in_check()==False):
            self.board[25]='-'
            self.board[24]='k'
            is_24_check = self.black_king_in_check()
            self.board[24]='-'
            self.board[23]='k'
            is_23_check = self.black_king_in_check()
            self.board[23] = '-'
            self.board[25] = 'k'
            if(is_24_check==False and is_23_check==False):
                self.black_queen_side_castle = True
                castled_move = Move(25,23,self.board)
                castled_move.is_castled=True
                legal_moves.append(castled_move)
        else:
            self.black_queen_side_castle = False

        #Check for Black King's King Side Castle
        if(piece=='k' and self.r2move==False and self.black_king_move == False and
           self.board[26]=='-' and self.board[27]=='-' and self.black_king_in_check()==False):
            self.board[25]='-'
            self.board[26]='k'
            is_26_check=self.black_king_in_check()
            self.board[26]='-'
            self.board[27]='k'
            is_27_check = self.black_king_in_check()
            self.board[25]='k'
            self.board[27]='-'
            if(is_27_check==False and is_26_check==False):
                self.black_king_side_castle=True
                castled_move = Move(25,27,self.board)
                castled_move.is_castled=True
                legal_moves.append(castled_move)
            
        else:
            self.black_king_side_castle=False

        #Check for White King's Queen Side Castle
        if(piece=='K' and self.R1move == False and self.white_king_move == False and 
           self.board[92]=='-' and self.board[93]=='-' and self.board[94]=='-' and self.white_king_in_check()==False):
            self.board[95]='-'
            self.board[94]='K'
            is_94_check = self.white_king_in_check()
            self.board[94]='-'
            self.board[93]='K'
            is_93_check = self.white_king_in_check()
            self.board[93] = '-'
            self.board[95] = 'K'
            if(is_94_check==False and is_93_check==False):
                self.white_queen_side_castle = True
                castled_move = Move(95,93,self.board)
                castled_move.is_castled=True
                legal_moves.append(castled_move)
        else:
            self.white_queen_side_castle = False

        #Check for White King's King Side Castle
        if(piece=='K' and self.r2move==False and self.white_king_move == False and
           self.board[96]=='-' and self.board[97]=='-' and self.white_king_in_check()==False):
            self.board[95]='-'
            self.board[96]='K'
            is_96_check=self.white_king_in_check()
            self.board[96]='-'
            self.board[97]='K'
            is_97_check = self.white_king_in_check()
            self.board[95]='K'
            self.board[97]='-'
            if(is_97_check==False and is_96_check==False):
                self.white_king_side_castle=True
                castled_move = Move(95,97,self.board)
                castled_move.is_castled=True
                legal_moves.append(castled_move)
        else:
            self.white_king_side_castle=False

        for i in range(len(pseudo)):
            final_index = pseudo[i]
            is_en_passant = False

            is_pawn_promotion = False

            is_king_safe = False

            new_move = Move(index,final_index,self.board)

            #EnPassant move check
            if(piece=='P' or piece=='p'):
                if(final_index==self.en_passant_target):
                    is_en_passant=True
            
            #Pawn Promotion check
            if( (piece=='P' and (final_index-20)//10==0) or (piece=='p' and (final_index-20)//10==7) ):
                is_pawn_promotion = True

            ep_captured = '-'
            #change the board to final state
            captured = self.board[final_index]
            self.board[final_index] = piece
            self.board[index]='-'

            #EnPassant is legal move
            if(is_en_passant==True):
                new_move.is_en_passant = True
                if(piece_color=="White"):
                    ep_captured = self.board[final_index+10]
                    self.board[final_index+10]='-'
                elif(piece_color=="Black"):
                    ep_captured = self.board[final_index-10]
                    self.board[final_index-10]='-'

            #Pawn Promotion is legal move or not
            if(is_pawn_promotion==True):
                new_move.is_promotion = True
                promotion=[]
                if(piece_color=="White"):
                    promotion = ['Q','R','B','N']
                elif(piece_color=="Black"):
                    promotion = ['q','r','b','n']
    
                for i in range(4):
                    self.board[index] = piece
                    self.board[final_index] = captured
                    pawn_prom_move = Move(index,final_index,self.board)
                    self.board[final_index]=promotion[i]
                    self.board[index]='-'

                    pawn_prom_move.pawn_promoted_to=promotion[i]
                    pawn_prom_move.move_id+=promotion[i]
                    pawn_prom_move.is_promotion=True

                    is_king_safe = False
                    if(piece_color=="White"):
                        if(self.white_king_in_check()==False):
                            is_king_safe = True
                    elif(piece_color=="Black"):
                        if(self.black_king_in_check()==False):
                            is_king_safe = True
            
                    if(is_king_safe):
                        legal_moves.append(pawn_prom_move)
                    
                self.board[index] = piece
                self.board[final_index] = captured
                continue

            #check if it is creating check or not
            if(piece_color=="White"):
                if(self.white_king_in_check()==False):
                    is_king_safe = True
            elif(piece_color=="Black"):
                if(self.black_king_in_check()==False):
                   is_king_safe = True
            
            if(is_king_safe):
                legal_moves.append(new_move)
            
            #reset the board to initial state
            self.board[index] = piece
            self.board[final_index] = captured
            if(is_en_passant==True):
                if(piece_color=="White"):
                    self.board[self.en_passant_target+10]=ep_captured
                elif(piece_color=="Black"):
                    self.board[self.en_passant_target-10]=ep_captured
        
        return legal_moves

