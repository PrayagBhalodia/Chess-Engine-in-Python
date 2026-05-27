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
        self.ai_stack = []

#-------------------------------------------------------------FOR AI TO MAKE AN UNMAKE A MOVE-----------------------------------------------------------------------------
    
    def make_ai_move(self, engine_move):
        # 1. PUSH TO STACK: Save ONLY the flags and the move object, NOT the whole board array!
        state_to_save = {
            'ep_target': self.en_passant_target,
            'half_moves': self.half_move_counter,
            'r1': self.r1move, 'r2': self.r2move,
            'R1': self.R1move, 'R2': self.R2move,
            'bk': self.black_king_move, 'wk': self.white_king_move,
            'b_k_castle': self.black_king_side_castle,
            'b_q_castle': self.black_queen_side_castle,
            'w_k_castle': self.white_king_side_castle,
            'w_q_castle': self.white_queen_side_castle,
            'move': engine_move 
        }
        self.ai_stack.append(state_to_save)
        
        initial = engine_move.start_idx
        final = engine_move.end_idx
        piece_to_move = engine_move.piece_moved
        
        # 2. Handle Castling Teleports
        if engine_move.is_castled:
            self.board[final] = piece_to_move
            self.board[initial] = '-'
            if final == 23: # Black Queen-Side
                self.board[24] = 'r'; self.board[21] = '-'
            elif final == 27: # Black King-Side
                self.board[26] = 'r'; self.board[28] = '-'
            elif final == 93: # White Queen-Side
                self.board[94] = 'R'; self.board[91] = '-'
            elif final == 97: # White King-Side
                self.board[96] = 'R'; self.board[98] = '-'

            if piece_to_move == 'k':
                self.black_king_move = True
                if final == 23: self.r1move = True
                elif final == 27: self.r2move = True
            elif piece_to_move == 'K':
                self.white_king_move = True
                if final == 93: self.R1move = True
                elif final == 97: self.R2move = True
            self.half_move_counter += 1
            self.en_passant_target = -1
                
        # 3. Handle Pawn Promotion
        elif engine_move.is_promotion:
            self.board[final] = engine_move.pawn_promoted_to
            self.board[initial] = '-'
            self.half_move_counter = 0
            
        # 4. Handle En Passant Deletions
        elif engine_move.is_en_passant:
            self.board[final] = piece_to_move
            self.board[initial] = '-'
            if piece_to_move == 'P':
                self.board[final + 10] = '-'
            elif piece_to_move == 'p':
                self.board[final - 10] = '-'
            self.half_move_counter = 0
                
        # 5. Normal Moves
        else: 
            self.board[final] = piece_to_move
            self.board[initial] = '-'
            if piece_to_move == 'p' or piece_to_move == 'P' or engine_move.piece_captured != '-':
                self.half_move_counter = 0
            else:
                self.half_move_counter += 1
        
        # Update en passant target
        self.en_passant_target = -1
        if piece_to_move == 'P' and initial - final == 20:
            self.en_passant_target = final + 10
        elif piece_to_move == 'p' and final - initial == 20:
            self.en_passant_target = final - 10

        # Update castling flags for non-castle moves
        if not engine_move.is_castled:
            if piece_to_move == 'r' and initial == 21: self.r1move = True
            elif piece_to_move == 'r' and initial == 28: self.r2move = True
            elif piece_to_move == 'R' and initial == 91: self.R1move = True
            elif piece_to_move == 'R' and initial == 98: self.R2move = True
            elif piece_to_move == 'k' and initial == 25: self.black_king_move = True
            elif piece_to_move == 'K' and initial == 95: self.white_king_move = True

        captured_piece = engine_move.piece_captured
        if captured_piece == 'r':
            if final == 21: self.r1move = True
            elif final == 28: self.r2move = True
        elif captured_piece == 'R':
            if final == 91: self.R1move = True
            elif final == 98: self.R2move = True

        self.counter += 1


    def unmake_ai_move(self):
        # 1. POP FROM STACK: Grab the old state
        old_state = self.ai_stack.pop()
        engine_move = old_state['move']
        
        # 2. Restore flags and counters directly
        self.en_passant_target = old_state['ep_target']
        self.half_move_counter = old_state['half_moves']
        self.r1move, self.r2move = old_state['r1'], old_state['r2']
        self.R1move, self.R2move = old_state['R1'], old_state['R2']
        self.black_king_move, self.white_king_move = old_state['bk'], old_state['wk']
        self.black_king_side_castle = old_state['b_k_castle']
        self.black_queen_side_castle = old_state['b_q_castle']
        self.white_king_side_castle = old_state['w_k_castle']
        self.white_queen_side_castle = old_state['w_q_castle']
        
        # 3. Manually reverse the board array using the move object
        initial = engine_move.start_idx
        final = engine_move.end_idx
        piece_moved = engine_move.piece_moved
        piece_captured = engine_move.piece_captured
        
        if engine_move.is_castled:
            self.board[initial] = piece_moved
            self.board[final] = '-'
            if final == 23: # Black Queen-Side
                self.board[21] = 'r'; self.board[24] = '-'
            elif final == 27: # Black King-Side
                self.board[28] = 'r'; self.board[26] = '-'
            elif final == 93: # White Queen-Side
                self.board[91] = 'R'; self.board[94] = '-'
            elif final == 97: # White King-Side
                self.board[98] = 'R'; self.board[96] = '-'
                
        elif engine_move.is_promotion:
            self.board[initial] = piece_moved # Put the pawn back!
            self.board[final] = piece_captured # Put whatever was captured back (could just be '-')
            
        elif engine_move.is_en_passant:
            self.board[initial] = piece_moved
            self.board[final] = '-'
            # Restore the captured pawn to its correct square!
            if piece_moved == 'P':
                self.board[final + 10] = 'p'
            elif piece_moved == 'p':
                self.board[final - 10] = 'P'
                
        else:
            # Normal Move Reversal
            self.board[initial] = piece_moved
            self.board[final] = piece_captured
            
        # 4. Tick the clock backward
        self.counter -= 1

#--------------------------------------------------BOARD TO STRING HELPER FUNCTION -------------------------------------------------------------
    def board_to_string(self):
        board_string = ""
        for i in range (120):
            if(self.board[i]!='x'):
                if(self.board[i]=='-'):
                    board_string+="0"
                else:
                    board_string+=self.board[i]
        ep_code = self.en_passant_target + 256 if self.en_passant_target == -1 else self.en_passant_target
        board_string += f"{ep_code:03d}"
        # BUG FIXING ENDS HERE
        board_string+=str(self.white_king_side_castle)+str(self.black_king_side_castle)+str(self.black_queen_side_castle)+str(self.white_queen_side_castle)
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

        #King check logic
        for i in range(8):
            if(self.board[index+step_moves[i]]=='k'):
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

        #King check logic
        for i in range(8):
            if(self.board[index+step_moves[i]]=='k'):
                return True

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
        if(piece=='k' and self.r1move == False and self.black_king_move == False and self.board[21]=='r' and
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
                castled_move = Move(25,23,self.board)
                castled_move.is_castled=True
                legal_moves.append(castled_move)

        #Check for Black King's King Side Castle
        if(piece=='k' and self.r2move==False and self.black_king_move == False and self.board[28]=='r' and
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
                castled_move = Move(25,27,self.board)
                castled_move.is_castled=True
                legal_moves.append(castled_move)

        #Check for White King's Queen Side Castle
        if(piece=='K' and self.R1move == False and self.white_king_move == False and self.board[91]=='R' and
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
                castled_move = Move(95,93,self.board)
                castled_move.is_castled=True
                legal_moves.append(castled_move)

        #Check for White King's King Side Castle
        if(piece=='K' and self.r2move==False and self.white_king_move == False and self.board[98]=='R' and
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
                castled_move = Move(95,97,self.board)
                castled_move.is_castled=True
                legal_moves.append(castled_move)
                
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
                    pawn_prom_move.move_id += promotion[i]
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