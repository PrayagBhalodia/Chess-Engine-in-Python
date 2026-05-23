class BoardState :
    def __init__ (self):
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

    #helper function for generating pseudo legal moves 
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

        #White Piece
        if(piece>'A' and piece<'Z'):
            if(self.board[index]>'a' and self.board[index]<'z' and self.board[index]!='x'):
                moves_list.append(index)

        #Black Piece
        if(piece>'a' and piece<'z'):
            if(self.board[index]>'A' and self.board[index]<'Z' ):
                moves_list.append(index)

        return moves_list


    def is_enemy(self,piece,index):
        #White Piece
        if(piece>'A' and piece<'Z'):
            if(self.board[index]>'a' and self.board[index]<'z' and self.board[index]!='x'):
                return True

        #Black Piece
        if(piece>'a' and piece<'z'):
            if(self.board[index]>'A' and self.board[index]<'Z' ):
                return True
                
        return False


    #generating pseudo legal moves 
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
            index = 10*init_y+20+init_x+1
            #Attack White Peices by Black Pawn moves
            if (self.board[index+11]!='-' and self.board[index+11]!='x' and ('A'<self.board[index+11] and 'Z'>self.board[index+11] )):
                moves.append(index+11)
            elif (self.board[index+9]!='-' and self.board[index+9]!='x' and ('A'<self.board[index+9] and 'Z'>self.board[index+9] )):
                moves.append(index+9)

            if(init_y==1):
                if(self.board[index+10]=='-'):
                    moves.append(index+10)
                    if(self.board[index+20]=='-'):
                        moves.append(index+20)
            elif(init_y<=6):
                #enPaussant check
                if(init_y==4):
                    if (self.board[index+11]=='-' and self.enPaussant[index+11]==True):
                        moves.append(index+11)
                    if (self.board[index+9]=='-' and self.enPaussant[index+9]==True):
                        moves.append(index+9)

                if(self.board[index+10]=='-'):
                    moves.append(index+10)

        #FOR WHITE PAWN PSEUDO LEGAL MOVES
        elif(piece=='P'):
            index = 10*init_y+20+init_x+1
            #Attack Black Peices by White Pawn moves
            if (self.board[index-11]!='-' and self.board[index-11]!='x' and ('a'<self.board[index-11] and 'z'>self.board[index-11] )):
                moves.append(index-11)
            elif (self.board[index-9]!='-' and self.board[index-9]!='x' and ('a'<self.board[index-9] and 'z'>self.board[index-9] )):
                moves.append(index-9)

            if(init_y==6):
                if(self.board[index-10]=='-'):
                    moves.append(index-10)
                    if(self.board[index-20]=='-'):
                        moves.append(index-20)
            elif(init_y>=1):
                #enPaussant check
                if(init_y==3):
                    if (self.board[index-11]=='-' and self.enPaussant[index-11]==True):
                        moves.append(index-11)
                    if (self.board[index-9]=='-' and self.enPaussant[index-9]==True):
                        moves.append(index-9)

                if(self.board[index-10]=='-'):
                    moves.append(index-10)

        return moves