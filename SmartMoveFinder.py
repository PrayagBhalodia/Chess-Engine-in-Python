import random
import numpy as np

pieceScore={
    'k':-1000 , 'K':1000,
    'p':-100 , 'P':100,
    'n':-320 , 'N':320,
    'b':-330 , 'B':330,
    'r':-500, 'R':500,
    'q':-900 , 'Q':900 
}

# For Pawn
pawn_white = np.array([
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5,  0, -5,  0,  0, -5,  0,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
])
pawn_black=pawn_white[::-1]

# For Knight 
knight_white = np.array([
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
])
knight_black=knight_white[::-1]

# For Bishop
bishop_white = np.array([
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
])
bishop_black=bishop_white[::-1]

# For Rook
rook_white = np.array([
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [ 0,  0,  0,  5,  5,  0,  0,  0]
])
rook_black=rook_white[::-1]

# For Queen
queen_white = np.array([
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [ 0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
])
queen_black=queen_white[::-1]

# For king
king_white = np.array([
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20]
])
king_black=king_white[::-1]


def BoardScore(board):
    score = 0
    for i in range(120):
        piece = board.board[i]
        if piece == 'x' or piece == '-':
            continue
        col = i % 10 - 1
        row = i // 10 - 2
        if col < 0 or col > 7 or row < 0 or row > 7:
            continue
        score += pieceScore[piece]
        if piece == 'r':   score -= rook_black[row][col]
        elif piece == 'R': score += rook_white[row][col]
        elif piece == 'b': score -= bishop_black[row][col]
        elif piece == 'B': score += bishop_white[row][col]
        elif piece == 'n': score -= knight_black[row][col]
        elif piece == 'N': score += knight_white[row][col]
        elif piece == 'p': score -= pawn_black[row][col]
        elif piece == 'P': score += pawn_white[row][col]
        elif piece == 'q': score -= queen_black[row][col]
        elif piece == 'Q': score += queen_white[row][col]
        elif piece == 'k': score -= king_black[row][col] 
        elif piece == 'K': score += king_white[row][col]

    if not board.white_king_move and not board.R1move and not board.R2move:
        score += 15   # white can still castle
    if not board.black_king_move and not board.r1move and not board.r2move:
        score -= 15   # black can still castle

    return score

def generate_legal_moves(board):
    moves_list = []
    if(board.counter%2==0):
        for i in range (120):
            if(board.board[i]!='x' and board.board[i]!='-' and board.board[i].isupper()==True):
                moves_list+=board.legal_moves(board.board[i],i%10-1,i//10-2)
    else:
        for i in range (120):
            if(board.board[i]!='x' and board.board[i]!='-' and board.board[i].islower()==True):
                moves_list+=board.legal_moves(board.board[i],i%10-1,i//10-2)

    return moves_list

def findBestMove (board):
    bestPlayerMove = MinMax_recursive(board,DEPTH,board.counter%2==0,-1e8,1e8)[1]
    return bestPlayerMove

#Min Max Algorithm with variable depth and along with alpha-beta pruning(fastest)
DEPTH = 4
def MinMax_recursive (board,depth,whiteToMove,alpha,beta):
    bestPlayerMove = None 

    if(depth==0):
        return BoardScore(board),None

    validMoves = generate_legal_moves(board)
    random.shuffle(validMoves)

    #White to Move
    if whiteToMove :
        maxScore = -1e8
        for playerMove in validMoves :
            board.make_ai_move(playerMove)
            score = MinMax_recursive(board,depth-1,False,alpha,beta)[0]
            board.unmake_ai_move()
            if maxScore < score :
                maxScore = score
                bestPlayerMove = playerMove
            alpha = max(alpha,maxScore)
            if beta <= alpha :
                break
        return maxScore,bestPlayerMove
        

        #Black to Move
    elif not whiteToMove : 
        minScore = 1e8
        for playerMove in validMoves:
            board.make_ai_move(playerMove)
            score = MinMax_recursive(board,depth-1,True,alpha,beta)[0]
            board.unmake_ai_move()
            if minScore > score :
                minScore = score
                bestPlayerMove = playerMove
            beta = min(beta,minScore)
            if beta <= alpha :
                break
        return minScore,bestPlayerMove

#Min Max Algorithm without recursion , depth = 2 and without alpha-beta pruning
def MinMax (board):
    validMoves = generate_legal_moves(board)
    random.shuffle(validMoves)
    bestValidMoves = [] 
    turn_multiplier = 1 if board.counter%2==0 else -1
    playerMaxScore = -1e8
    for playerMove in validMoves:
        board.make_ai_move(playerMove)
        opponentValidMoves = generate_legal_moves(board)
        opponentMinScore = 1e8
        for opponentMove in opponentValidMoves:
            board.make_ai_move(opponentMove)
            score = turn_multiplier * BoardScore(board)
            board.unmake_ai_move()

            if(score < opponentMinScore):
                opponentMinScore = score
        
        if(opponentMinScore > playerMaxScore):
            playerMaxScore = opponentMinScore
            bestValidMoves = []
            bestValidMoves.append(playerMove)

        elif(opponentMinScore == playerMaxScore):
            bestValidMoves.append(playerMove)   
        board.unmake_ai_move()

    index = random.randint(0,len(bestValidMoves)-1)
    return bestValidMoves[index]




#Always Takes a Piece if Possible Without thinking about consiquences
def greedyMove (board):
    turn_multiplier = 1 if board.counter%2==0 else -1
    playerScore = -1000000
    validMoves = generate_legal_moves(board)
    random.shuffle(validMoves)

    bestAImove = validMoves[0]
    for moves in validMoves:
        board.make_ai_move(moves)
        score = turn_multiplier * BoardScore(board)
        if(score>playerScore):
            bestAImove = moves
            playerScore = score
        board.unmake_ai_move()

    return bestAImove

#Makes a random move from all the legal moves possible
def random_AI_moves(move_list):
    if(len(move_list)==0):
        return -1
    return random.randint(0,len(move_list)-1)