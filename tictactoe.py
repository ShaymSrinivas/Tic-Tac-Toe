from numpy import *

#TODO: remove, this is a standin until there's sufficient interaction.
game_state = array( [[-1,0,1],[1,-1,0],[1,0, -1]] )

def check_for_win(board):
    '''
    Assume a valid board configuration, i.e. only 0 or 1 winners
    '''

    I = identity(3) # define 3x3 identity matrix
    ones = array( [[1,1,1]] ) # define 1s vector (1x3 matrix)
    column = row = 0 # numpy indices start at 0, not 1
    #check the columns
    while column < 3:
        column_sum = ones.dot(board).dot(I[:,column])
        if column_sum == 3:
            return 'x wins1'
        elif column_sum == -3:
            return 'o wins1'
        column += 1
    # Check the rows
    while row < 3:
        row_sum = ones.dot(board.T).dot(I[:,row])
        if row_sum == 3:
            return 'x wins'
        elif row_sum == -3:
            return 'o wins'
        row += 1
    # Check the diaganols
    if trace(board) == 3:
        return 'x wins'
    elif trace(board) == -3:
        return 'o wins'
    elif trace(flipud(board)) == 3:
        return 'x wins'
    elif trace(flipud(board)) == -3:
        return 'o wins'
    else: return 'no winner, keep playing'

def human_turn():
    # Assume humans are X (and X equals 1)
    row = raw_input("Your turn! Enter a row.")
    column = raw_input("Your turn! Enter a column.")
    
    if check_position(row, column):
        game_state[row,column] = 1 # TODO generalize to Xs or Os
    else:
        print "That spots already taken! Please pick another spot."
        human_turn()

def check_position(row, column):
    if game_state[row,column] == 0: # position is free
        return True
    else: # position taken
        return False

print game_state
human_turn()
print game_state
result = check_for_win(game_state)
print result
