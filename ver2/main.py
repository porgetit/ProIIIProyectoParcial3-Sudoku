from generator import BoardGenerator

board = BoardGenerator(3).generate()
board = [[board.var(row, col).get_value() if board.var(row, col).is_assigned() else 0 for col in range(9)] for row in range(9)]
for row in board:
    print(row)
    
'''
Lo de arribe es solo para comprobar que tanto el obj board como el var funcionen correctamente, al menos en lo basico
'''