# Author: Joseph Nix
# nixjdm@terminallabs.com
# 512-348-8043

from numpy import array, count_nonzero, flipud, identity, nonzero, trace, transpose, where, zeros
from random import SystemRandom
#TODO: remove, this is a standin until there's sufficient interaction.


class TicTacToe(object):
    def __init__(self, cli = None):
        '''
        Set initial game conditions: empty board, whether human chose to go first, if human chose Xs or Os.
        
        start game
        '''
        self.winner = None
        self.center = [1,1]
        self.corners = [[0,0], [0,2], [2,0], [2,2]]
        self.edges = [[0,1], [1,0], [1,2], [2,1]]
        self.game_state = zeros((3,3)) # Initialize empty board
        # self.game_state = array( [[0,-1,1],[-1,-1,1],[1,1,-1]] )
        if cli:
            self.cli_game()
            self.cli = True
        else:
            self.cli = False

    def cli_game(self):
        '''
        Play game via Command Line Interface
        '''
        ##NOTE: Not sanitizing user input right now. Will likely do away with the cli when gui implemented.
        self.player_choice = raw_input("Do you want to be Xs or Os? (x/o)")
        # self.player_choice = SystemRandom().choice(['x','o'])
        # X equals 1, O equals -1
        if self.player_choice == 'x':
            self.human_marker = 1
            printx('human is X')
        else:
            self.human_marker = -1
            printx('human is O')
        self.computer_marker = -self.human_marker

        initial_move_choice = raw_input("Do you want to go first? (y/n)")
        # initial_move_choice = SystemRandom().choice(['n'])
        if initial_move_choice == 'y':
            printx('human goes first')
            self.human_turn()
        else:
            printx('computer goes first')
            self.computer_turn()

    def gui_move(self, player_choice, turn_number, game_state):
        '''
        Play game via GUI (using more than just this module)
        '''
        # X equals 1, O equals -1
        self.player_choice = player_choice
        self.game_state = array(game_state)
        print 'game_state', self.game_state
        print 'game_state', array(self.game_state)

        # set who is x / who is o
        if self.player_choice == 'x':
            self.human_marker = 1
            printx('human is X')
        elif player_choice == 'o':
            self.human_marker = -1
            printx('human is O')
        self.computer_marker = -self.human_marker

        ##TODO: check for win
        # It's always the computer's turn next, regardless of which game turn it is
        self.computer_turn() ##TODO: follow with a check for win and return game state / new position

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
        for column in range(3):
            sum = ones.dot(self.game_state).dot(I[:,column])
            if sum == marker*3: # column sum = 3 or -3 is a winning condition for marker 1 or -1 respectively
                return 'win'

        # Check the rows
        for row in range(3):
            sum = ones.dot(self.game_state.T).dot(I[:,row])
            if sum == marker*3: # row sum = 3 or -3 is a winning condition for marker 1 or -1 respectively
                return 'win'

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
        else:
            return 'no winner'

    def human_turn(self):
        '''
        Prompt for human move, place move, check for an end game scenario, call computer_turn if game isn't over.

        Not run from a GUI game
        '''
        move = []
        move.extend( raw_input("your turn! Enter a row.") )
        move.extend( raw_input("your turn! Enter a column.") )
        # move = self.random_move()
        # Place move
        if self.is_available(move):
            self.game_state[move[0],move[1]] = self.human_marker
            printx(self.game_state)
        else:
            printx( "That spots already taken! Please pick another spot.")
            self.human_turn()
        # check for win
        win_state = self.check_for_win(self.human_marker)
        if win_state == 'win':
            self.winner = 'human'
            printx('game over - you won!')
        elif win_state == 'tie':
            self.winner = 'tie'
            printx("game over - there's a tie")
        elif win_state == 'no winner':
            printx('should now keep playing')
            # computer's turn
            self.computer_turn()

    def computer_turn(self):
        '''
        Play computer move, place move, check for an end game scenario, call human_turn if game isn't over.

        If gui game, do not call human_turn next, instead return state info
        '''
        # check first if human caused a tie
        if not self.cli:
            self.win_state = self.check_for_win(self.human_marker)
            if self.win_state == 'win':
                self.winner = 'human'
                printx('game over - you won!')
                return
            elif self.win_state == 'tie':
                self.winner = 'tie'
                printx("game over - there's a tie")
                return
            elif self.win_state == 'no winner':
                printx('should now keep playing')

            assert count_nonzero(self.game_state) != 9 # if there's a tie, we should not get here

        move = self.computer_ai() # calculate next computer move
        self.last_cp_move = move
        if self.is_available(move): #TODO: change to assert later (ai will always pass an available position)
            self.game_state[move[0],move[1]] = self.computer_marker
            printx(self.game_state)
        else:
            printx("That spots already taken! Please pick another spot.")
            self.computer_turn()

        # check for win
        self.win_state = self.check_for_win(self.computer_marker)
        if self.cli:
            if self.win_state == 'win':
                self.winner = 'computer'
                printx('game over - the computer won!')
            elif self.win_state == 'tie':
                self.winner = 'tie'
                printx("game over - there's a tie")
            elif self.win_state == 'no winner':
                printx('should now keep playing')
                self.human_turn()
        else: # gui game
            if self.win_state == 'win':
                self.winner = 'computer'
                printx('game over - the computer won!')
            elif self.win_state == 'tie':
                self.winner = 'tie'
                printx("game over - there's a tie")
            elif self.win_state == 'no winner':
                printx('should now keep playing')

    def computer_ai(self):
        '''
        Calculate which move to play next.
        '''
        ##NOTE: Listing odd moves first (computer starts the game) to aid in reading the algorithm.
        ##This way you can read sequential code for sequential computer moves.

        ### Computer first sequence ###
        # 1st move of the game:
        if count_nonzero(self.game_state) == 0:
            return self.first_move()

        # 3rd move of the game:
        elif count_nonzero(self.game_state) == 2:
            return self.third_move()
        
        # 5th move of the game:
        elif count_nonzero(self.game_state) == 4:
            return self.fifth_move()

        # 2th move of the game:
        elif count_nonzero(self.game_state) == 1:
            return self.second_move()

        # 4th move of the game:
        elif count_nonzero(self.game_state) == 3:
            return self.fourth_move()

        # late moves (finishing the game):
        else:
            printx('play late move')
            return self.late_move()

    ## Listed in alternating order to better match actual gameplay (computer will either move on odd turns, or even turns)
    def first_move(self):
        choices = self.corners + [self.center] # coordinates of first move choices, no edges
        next_move = SystemRandom().choice(choices)
        return next_move

    def third_move(self):
        choices = []
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
            if human_move in self.edges: # human moved on an edge
                if human_move in self.adjacent_cells(computer_move): # if the human played right next to the computer
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
            if human_move in self.corners:
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

    def fifth_move(self):
        choices = []
        if self.winning_opportunity(): # first check for a winning opportunity, and just take it if it exists
            return self.winning_opportunity()
        elif self.game_state[1,1] == self.computer_marker: # one of computer's two moves is the center
            if self.blocking_opportunity():
                return self.blocking_opportunity()
            else:
                for corner in self.corners: # 3rd move would necessarily be a corner
                    if (self.is_available(corner) and # check if this corner is available
                        all(self.game_state[cell[0], cell[1]] != self.human_marker for cell in self.adjacent_cells(corner)) ): # all adjacent cells of this corner have not been marked by a human
                        choices.append(corner)
                next_move = SystemRandom().choice(choices) # take the only free corner not touching the opponent
                return next_move
        elif self.blocking_opportunity():
            return self.blocking_opportunity()
        else: # computer is on 2 corners, and has no blocking or winning opportunities
            available_corners = 0
            for corner in self.corners:
                if self.is_available(corner):
                    available_corners +=1
            if available_corners == 2: # two corners open
                choices.append([1,1])
                for corner in self.corners:
                    # only one corner will pass this test
                    if (self.is_available(corner) and # check if this corner is available.
                        all(self.game_state[cell[0], cell[1]] != self.human_marker for cell in self.adjacent_cells(corner)) ): # all adjacent cells of this corner have not been marked by a human
                        choices.append(corner)
            elif available_corners == 1: # one corner open
                for corner in self.corners:
                    if self.is_available(corner): # only one corner is available
                        choices.append(corner)
            else:
                raise error('missed something!')
            next_move = SystemRandom().choice(choices) # take the only free corner not touching the opponent
            return next_move

    def second_move(self):
        choices = []
        human_move = where(self.game_state == self.human_marker)
        human_move = [human_move[0][0], human_move[1][0]]
        if human_move == self.center:
            choices = self.corners
        elif human_move in self.corners:
            choices.append(self.center)
        else: # human played on edge
            choices.append(self.center)
        next_move = SystemRandom().choice(choices)
        return next_move

    def fourth_move(self):
        choices = []

        if self.blocking_opportunity():
            return self.blocking_opportunity()

        elif (((self.game_state[0,0] and self.game_state[2,2]) or (self.game_state[0,2] and self.game_state[2,0])) == self.human_marker) and (self.game_state[1,1] == self.computer_marker): # computer on center, both human_markers on opposite corners from each other
            choices = self.edges

        elif self.game_state[1,1] == self.computer_marker: # computer in the center
            human_marker_coordinates = transpose(where(self.game_state == self.human_marker))
            formated_correctly = []
            for x in human_marker_coordinates:
                formated_correctly.append([x[0], x[1]])
            human_marker_coordinates = formated_correctly
            if all(cell in self.edges for cell in human_marker_coordinates ): # all human markers are on edges
                for corner in self.corners:
                    if (self.is_available(corner) and # check if this corner is available.
                        all(self.game_state[cell[0], cell[1]] == self.human_marker for cell in self.adjacent_edges(corner)) ): # check if all adjacent edges of corner are human_markers
                        choices.append(corner) # pick corner adjacent to human_marker
            elif any(cell in self.edges for cell in human_marker_coordinates ): # one human marker is on an edge, one human marker is on a corner
                # pick corner adjacent to human edge
                for corner in self.corners:
                    if (self.is_available(corner) and # check if this corner is available.
                        any(self.game_state[cell[0], cell[1]] == self.human_marker for cell in self.adjacent_edges(corner)) ): # check if corner is adjacent to an edge human_marker
                        choices.append(corner) # pick corner adjacent to human_marker

        elif self.game_state[1,1] == self.human_marker: # human in the center
            for corner in self.corners:
                if self.is_available(corner): # simply pick a free corner
                    choices.append(corner)

        else: # the move doesn't matter, just play this one randomly
            raise error('missed something!')

        if not choices: # no special cases listed above, this move can go anywhere
            return self.random_move()

        next_move = SystemRandom().choice(choices)
        return next_move

    def late_move(self):
        choices = []
        if self.winning_opportunity(): # first check for a winning opportunity, and just take it if it exists
            return self.winning_opportunity()
        elif self.blocking_opportunity(): # block if you can't win
            return self.blocking_opportunity()
        else: # the move doesn't matter, just play this one randomly
            return self.random_move()

    def random_move(self):
        '''
        Return coordinates of a random free space
        '''
        choices = transpose(where(self.game_state==0))
        next_move = SystemRandom().choice(choices) # take one of the two far corners
        return next_move

    def winning_opportunity(self):
        '''
        Return coordinates that will win the game if it exists, False otherwise.
        '''
        # Check the columns
        choices = []
        I = identity(3) # Define 3x3 identity matrix
        ones = array( [[1,1,1]] ) # Define 1s vector (1x3 matrix)
        for column in range(3):
            sum = ones.dot(self.game_state).dot(I[:,column])
            if sum == self.computer_marker*2: # column sum = -2 is a winning opportunity for computer
                choices.append([ where(self.game_state[:,column]==0)[0][0], column ])

        # Check the rows
        for row in range(3):
            sum = ones.dot(self.game_state.T).dot(I[:,row])
            if sum == self.computer_marker*2: # row sum = -2 is a winning opportunity for computer
                choices.append([ row, where(self.game_state[row,:]==0)[0][0] ])

        # Check the diaganols
        sum = trace(self.game_state)
        if sum == self.computer_marker*2: # diaganol sum = -2 is a winning opportunity for computer
            for i in range (3):
                if self.game_state[i,i] == 0:
                    choices.append([i,i])
        sum = trace(flipud(self.game_state))
        if sum == self.computer_marker*2: # opposite diaganol sum = -2 is a winning opportunity for computer.
            for i in [[0,2], [1,1], [2,0]]:
                if self.game_state[i[0], i[1]] == 0:
                    choices.append(i)

        # if there are any winning opportunities, choose one randomly
        if choices:
            next_move = SystemRandom().choice(choices)
            return next_move
        else:
            return False

    def blocking_opportunity(self):
        '''
        Return coordinates that will block a potential win by the opponentif it exists, False otherwise.
        This code is very similar to winning_opportunity()
        '''
        # Check the columns
        choices = []
        I = identity(3) # Define 3x3 identity matrix
        ones = array( [[1,1,1]] ) # Define 1s vector (1x3 matrix)
        for column in range(3):
            sum = ones.dot(self.game_state).dot(I[:,column])
            if sum == self.human_marker*2: # column sum = -2 is a winning opportunity for human
                choices.append([ where(self.game_state[:,column]==0)[0][0], column ])

        # Check the rows
        for row in range(3):
            sum = ones.dot(self.game_state.T).dot(I[:,row])
            if sum == self.human_marker*2: # row sum = -2 is a winning opportunity for human
                choices.append([ row, where(self.game_state[row,:]==0)[0][0] ])

        # Check the diaganols
        sum = trace(self.game_state)
        if sum == self.human_marker*2: # diaganol sum = -2 is a winning opportunity for human
            for i in range (3):
                if self.game_state[i,i] == 0:
                    choices.append([i,i])
        sum = trace(flipud(self.game_state))
        if sum == self.human_marker*2: # opposite diaganol sum = -2 is a winning opportunity for human
            for i in [[0,2], [1,1], [2,0]]:
                if self.game_state[i[0], i[1]] == 0:
                    choices.append(i)

        # if there are any  opportunities, choose one randomly
        if choices:
            next_move = SystemRandom().choice(choices)
            return next_move
        else:
            return False

    def adjacent_cells(self, corner):
        '''
        Return a list of coordinates for adjacent cells of the form [ [x0,y0], [x1,y1], ... ].
        Input must be a corner space.
        '''
        assert corner in self.corners
        choices = []

        if corner in self.corners:
            choices.append([corner[0], 1 ])
            choices.append([1, corner[1] ])
            choices.append([1, 1 ])
            
        return choices

    def adjacent_edges(self, corner):
        '''
        Return a list of coordinates for adjacent edges of the form [ [x0,y0], [x1,y1], ... ].
        Input must be a corner space.
        '''
        assert corner in self.corners
        return [item for item in self.adjacent_cells(corner) if item not in [[1,1]]]        

    def is_available(self, cell):
        '''
        Check if the given coordinates on the board are free.

        Return True if free, False if not Free
        '''
        if self.game_state[cell[0],cell[1]] == 0: # position is free
            return True
        else: # position taken
            return False

def printx(message):
    # comment out next line to remove all prints
    print message
    return


if __name__ == '__main__':
## used during build for testing
    winner = None
    i=0
    while winner != 'human':
        game = TicTacToe(cli=True)
        prints(game.game_state)
        winner = game.winner
        printx('winner'+str(i)+'  = ', winner)
        i += 1
