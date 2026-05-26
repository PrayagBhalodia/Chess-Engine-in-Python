import random

pieceScore={
    'k':-1000 , 'K':1000,
    'p':-10 , 'P':10,
    'n':-30 , 'N':30,
    'b':-30 , 'B':30,
    'r':-50 , 'R':50,
    'q':-90 , 'Q':90 
}

def BoardScore (board):
    score = 0 
    for i in range(120):
        if(board.board[i]!='x' and board.board[i]!='-'):
            score+=pieceScore[board.board[i]]
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


def random_AI_moves(move_list):
    if(len(move_list)==0):
        return -1
    return random.randint(0,len(move_list)-1)