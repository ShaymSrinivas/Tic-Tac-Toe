from numpy import array, count_nonzero, flipud, identity, trace, zeros

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
        self.player_choice = raw_input("Do you want to be Xs or Os? (x/o)")

        # X equals 1, O equals -1
        if self.player_choice == 'x':
            self.player_marker = 1
        else:
            self.player_marker = -1
        self.computer_marker = -self.player_marker

        if initial_move_choice == 'y':
            self.human_turn()
        else:
            self.computer_turn()

    def check_for_win(self):
        '''
        Assume a valid board configuration, i.e. only 0 or 1 winners
        '''

        I = identity(3) # Define 3x3 identity matrix
        ones = array( [[1,1,1]] ) # Define 1s vector (1x3 matrix)
        column = row = 0 # numpy indices start at 0, not 1
        # Check the columns
        while column < 3:
            column_sum = ones.dot(self.game_state).dot(I[:,column])
            if column_sum == 3:
                return 'win'
            elif column_sum == -3:
                return 'win'
            column += 1
        # Check the rows
        while row < 3:
            row_sum = ones.dot(self.game_state.T).dot(I[:,row])
            if row_sum == 3:
                return 'win'
            elif row_sum == -3:
                return 'win'
            row += 1
        # Check the diaganols
        if trace(self.game_state) == 3:
            return 'win'
        elif trace(self.game_state) == -3:
            return 'win'
        elif trace(flipud(self.game_state)) == 3:
            return 'win'
        elif trace(flipud(self.game_state)) == -3:
            return 'win'
        # Check for tie game
        elif count_nonzero(self.game_state) == 9:
            return 'tie'
        # Keep playing
        else: return 'no winner'

    def human_turn(self):
        '''
        Prompt for human move, place move, check for an end game scenario, call computer_turn if game isn't over.
        '''
        row = raw_input("your turn! Enter a row.")
        column = raw_input("your turn! Enter a column.")
        # place move
        if self.check_position(row, column):
            self.game_state[row,column] = self.player_marker
            print self.game_state
        else:
            print "That spots already taken! Please pick another spot."
            self.human_turn()
        # check for win
        win_state = self.check_for_win()
        if win_state == 'win':
            print 'game over - someone won!'
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
        row = raw_input("computer's turn! Enter a row.")
        column = raw_input("computer's turn! Enter a column.")
        # place move
        if self.check_position(row, column):
            self.game_state[row,column] = self.computer_marker
            print self.game_state
        else:
            print "That spots already taken! Please pick another spot."
            self.computer_turn()
        # check for win
        win_state = self.check_for_win()
        if win_state == 'win':
            print 'game over - someone won!'
        elif win_state == 'tie':
            print "game over - there's a tie"
        elif win_state == 'no winner':
            print 'should now keep playing'
            # computer's turn
            self.human_turn()

    def check_position(self, row, column):
        '''
        Check if the given coordinates on the board are free.

        Return True if free, False if not Free
        '''
        if self.game_state[row,column] == 0: # position is free
            return True
        else: # position taken
            return False


game = TicTacToe()
print game.game_state
game.human_turn()
print game.game_state
