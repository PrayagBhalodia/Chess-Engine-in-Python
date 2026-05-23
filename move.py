class Move :
    def __init__(self,start_idx, end_idx, board):
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.piece_moved = board[start_idx]
        self.piece_captured = board[end_idx]

        self.is_en_passant = False
        self.is_castled = False
        self.is_promotion = False
        self.pawn_promoted_to = '-'
        self.move_id = self.piece_moved+str(self.start_idx*10000 + self.end_idx)+self.piece_captured

    def __eq__(self, other):
        if isinstance(other, Move):
            if self.move_id == other.move_id:
                return True
        return False
    

