from numpy import array, count_nonzero, flipud, identity, nonzero, trace, where, zeros
from random import SystemRandom
#TODO: remove, this is a standin until there's sufficient interaction.


class TicTacToe(object):
    def __init__(self):
        '''
        Set initial game conditions: empty board, whether human chose to go first, if human chose Xs or Os.
        
        start game
        '''
        self.game_state = zeros((3,3)) # Initialize empty board
        # self.game_state = array( [[0,-1,1],[-1,-1,1],[1,1,-1]] )

        ##NOTE: Not sanitizing user input right now. Will likely do away with the cli when gui implemented.
        initial_move_choice = raw_input("Do you want to go first? (y/n)")
        if initial_move_choice == 'y':
            self.first_player = 'human'
        else:
            self.first_player = 'computer'
        self.player_choice = raw_input("Do you want to be Xs or Os? (x/o)")

        # X equals 1, O equals -1
        if self.player_choice == 'x':
            self.human_marker = 1
        else:
            self.human_marker = -1
        self.computer_marker = -self.human_marker

        if initial_move_choice == 'y':
            self.human_turn()
        else:
            self.computer_turn()

    def check_for_win(self, marker):
        '''
        Assume a valid board configuration, i.e. only 0 or 1 winners.
        Only check if the player that just moved won.
        '''
        assert marker == 1 or marker == -1
        I = identity(3) # Define 3x3 identity matrix
        ones = array( [[1,1,1]] ) # Define 1s vector (1x3 matrix)
        column = row = 0 # numpy indices start at 0, not 1

        # Check the columns
        while column < 3:
            sum = ones.dot(self.game_state).dot(I[:,column])
            if sum == marker*3: # column sum = 3 or -3 is a winning condition for marker 1 or -1 respectively
                return 'win'
            column += 1

        # Check the rows
        while row < 3:
            sum = ones.dot(self.game_state.T).dot(I[:,row])
            if sum == marker*3: # row sum = 3 or -3 is a winning condition for marker 1 or -1 respectively
                return 'win'
            row += 1

        # Check the diaganols
        sum = trace(self.game_state)
        if sum == marker*3: # diaganol sum = 3 or -3 is a winning condition for marker 1 or -1 respectively
            return 'win'
        sum = trace(flipud(self.game_state))
        if sum == marker*3: # opposite diaganol sum = 3 or -3 is a winning condition for marker 1 or -1 respectively
            return 'win'

       # Check for tie game
        if count_nonzero(self.game_state) == 9:
            return 'tie'
        # Keep playing
        else: return 'no winner'

    def human_turn(self):
        '''
        Prompt for human move, place move, check for an end game scenario, call computer_turn if game isn't over.
        '''
        move = []
        move.extend( raw_input("your turn! Enter a row.") )
        move.extend( raw_input("your turn! Enter a column.") )
        # place move
        if self.is_available(move):
            self.game_state[move[0],move[1]] = self.human_marker
            print self.game_state
        else:
            print "That spots already taken! Please pick another spot."
            self.human_turn()
        # check for win
        win_state = self.check_for_win(self.human_marker)
        if win_state == 'win':
            print 'game over - you won!'
        elif win_state == 'tie':
            print "game over - there's a tie"
        elif win_state == 'no winner':
            print 'should now keep playing'
            # computer's turn
            self.computer_turn()

    def computer_turn(self):
        '''
        Play computer move, place move, check for an end game scenario, call human_turn if game isn't over.

        ##TODO: Computer move is actually manual (human) right now, will add AI after game flow is finished
        '''
        move = self.computer_ai()
        print 'move', move
        if self.is_available(move): #TODO: change to assert later (ai will always pass an available position)
            self.game_state[move[0],move[1]] = self.computer_marker
            print self.game_state
        else:
            print "That spots already taken! Please pick another spot."
            self.computer_turn()
        # check for win
        win_state = self.check_for_win(self.computer_marker)
        if win_state == 'win':
            print 'game over - the computer won!'
        elif win_state == 'tie':
            print "game over - there's a tie"
        elif win_state == 'no winner':
            print 'should now keep playing'
            # computer's turn
            self.human_turn()

    def computer_ai(self):
        '''
        Calculate which move to play next.
        '''
        ##NOTE: Listing odd moves first (computer starts the game) to aid in reading the algorithm.
        ##This way you can read sequential code for sequential computer moves.

        choices = []

        ### Computer first sequence ###
        # 1st move of the game:
        if count_nonzero(self.game_state) == 0:
            choices = [[0,0], [1,1], [0,2], [2,0], [2,2]] # coordinates of first move choices, no edges
            next_move = SystemRandom().choice(choices)
            return next_move

        # 3rd move of the game:
        elif count_nonzero(self.game_state) == 2:
            computer_move = where(self.game_state == self.computer_marker)
            computer_move = [computer_move[0][0], computer_move[1][0]]
            human_move = where(self.game_state == self.human_marker)
            human_move = [human_move[0][0], human_move[1][0]]

            if human_move == [1,1]: # human moved in the center (computer must have moved in a corner)
                # next computer move is the opposite corner of first computer move
                next_move_row = (computer_move[0] + 2) % 4 # go from row 0 to 2, or 2 to 0
                next_move_column = (computer_move[1] + 2) % 4 # go from column 0 to 2, or 2 to 0
                next_move = [next_move_row, next_move_column]
                return next_move

            if computer_move != [1,1]: # computer moved on a corner
                if self.is_edge(human_move): # human moved on an edge
                    if human_move in self.adjacent_coordinates(computer_move): # if the human played right next to the computer
                        next_move = [1,1] # take the center
                        return next_move
                    else: # human is on edge away from computer
                        choices.append([ (computer_move[0] + 2) % 4, computer_move[1] ])
                        choices.append([ computer_move[0], (computer_move[1] + 2) % 4 ])
                        next_move = SystemRandom().choice(choices) # take one of the corners adjacent to the human
                        return next_move
                else: # human moved on one of the other 3 corners
                    for corner in [[0,0], [0,2], [2,0], [2,2]]:
                        if self.is_available(corner):
                            choices.append(corner)
                    next_move = SystemRandom().choice(choices) # take any available corner
                    return next_move

            else: # computer moved in the center
                if self.is_corner(human_move):
                    # next move is opposite corner of human move
                    next_move_row = (human_move[0] + 2) % 4 # go from row 0 to 2, or 2 to 0
                    next_move_column = (human_move[1] + 2) % 4 # go from column 0 to 2, or 2 to 0
                    next_move = [next_move_row, next_move_column]
                    return next_move
                else: # human move is an edge
                    if human_move[0] == 1:
                        choices.append([ 0, (human_move[1] + 2) % 4 ])
                        choices.append([ 2, (human_move[1] + 2) % 4 ])
                    else: # human_move[1] == 1
                        choices.append([ (human_move[0] + 2) % 4, 0 ])
                        choices.append([ (human_move[0] + 2) % 4, 2 ])
                    next_move = SystemRandom().choice(choices) # take one of the two far corners
                    return next_move

                        
                        

                    

        # 5th move of the game:
        elif count_nonzero(self.game_state) == 4:
            pass

        # 7th move of the game:
        elif count_nonzero(self.game_state) == 6:
            pass

        # last (9th) move of the game:
        elif count_nonzero(self.game_state) == 8:
            pass

    def random_move(self):
        '''
        Return coordinates of a random free space
        '''
        choices = transpose(nonzero(self.game_state))
        next_move = SystemRandom().choice(choices) # take one of the two far corners
        return next_move

    def winning_opportunity(self):
        '''
        Return coordinates that will win the game if it exists, False otherwise.
        '''
        # Check the columns
        choices = []
        while column < 3:
            sum = ones.dot(self.game_state).dot(I[:,column])
            if sum == self.computer_marker*2: # column sum = -2 is a winning opportunity for computer
                choices.append([ where(self.game_state[:,column]==0)[0][0], column ])
            column += 1

        # Check the rows
        while row < 3:
            sum = ones.dot(self.game_state.T).dot(I[:,row])
            if sum == self.computer_marker*2: # row sum = -2 is a winning opportunity for computer
                choices.append([ row, where(self.game_state[row,:]==0)[0][0] ])
            row += 1

        # Check the diaganols
        sum = trace(self.game_state)
        if sum == self.computer_marker*2: # diaganol sum = -2 is a winning opportunity for computer
            for i in range (3):
                if self.game_state[i,i] == 0:
                    choices.append([i,i])
        sum = trace(flipud(self.game_state))
        if sum == self.computer_marker*2: # opposite diaganol sum = -2 is a winning opportunity for computer.
            if self.game_state[0,2] == 0:
                choices.append([0,2])
            else: # [1,1] was caught in the first diaganol check, only one other option
                choices.append([2,0])

        next_move = SystemRandom().choice(choices) # take one of the two far corners
        return next_move

    def adjacent_coordinates(self, cell):
        '''
        Return a list of coordinates for adjacent cells of the form [ [x0,y0], [x1,y1], ... ].
        Currently only returns corner works if input is a corner space.
        '''
        adjacent_cells = []

        if self.is_corner(cell):
            adjacent_cells.append([cell[0], 1 ])
            adjacent_cells.append([1, cell[1] ])
            adjacent_cells.append([1, 1 ])
            
        elif self.is_edge(cell): ##NOTE: not used right now, haven't checked for accuracy #TODO: check (fix), or remove if not needed
            print "in adjancent_cell - is edge. not handled!"
            adjacent_cells.append([ cell[0], 1 ])
            adjacent_cells.append([ 1, cell[1] ])
            adjacent_cells.append([ 1, 1 ])

        return adjacent_cells

    def is_corner(self, cell):
        '''
        Return whether the input coordinates are a corner space
        '''
        if cell == ([0,0] or [0,2] or [2,0] or [2,2]):
            return True
        else:
            return False

    def is_edge(self, cell):
        '''
        Return whether the input coordinates are an edge space
        '''
        if cell == ([0,1] or [1,0] or [1,2] or [2,1]):
            return True
        else:
            return False

    def is_available(self, cell):
        '''
        Check if the given coordinates on the board are free.

        Return True if free, False if not Free
        '''
        print 'cell', cell
        print 'game_state', self.game_state
        print 'self.game_state[cell[0],cell[1]]', self.game_state[cell[0],cell[1]]
        if self.game_state[cell[0],cell[1]] == 0: # position is free
            return True
        else: # position taken
            return False

game = TicTacToe()
print game.game_state
