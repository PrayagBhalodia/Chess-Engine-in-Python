import random

def random_AI_moves(move_list):
    if(len(move_list)==0):
        return -1
    return random.randint(0,len(move_list)-1)