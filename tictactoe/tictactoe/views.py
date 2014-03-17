from django.shortcuts import render_to_response
from tictactoe import TicTacToe

human = 'x' ##TODO: let human choose wether to be x or o. Right now, human is always x.
marker = 1

def index( request ):
    '''
    Render initial page with no moves present.
    '''
    positions = ['c0',
             'c1',
             'c2',
             'c3',
             'c4', 
             'c5', 
             'c6',
             'c7',
             'c8',
             'c9', #indicates if computer goes first              
             ]
    moves = {}
    for position in positions:
        moves[position] = 0
    # generate list of urls for the links on each cell
    # when clicked, a cell's url should coorespond to the current game state plus that move
    url_list = []
    for cell in range(10):
        url ='s?'
        for position in positions:
            # adding substring that corresponds to game state / move
            url += position + '='
            if position[1] == str(cell):
                url += str( marker) # the player's move. 1 or -1
            else:
                url += str( moves[position]) #should be 0
                
            if position != 'c9': # add '&' to concatenate next substring
                url += '&'
        url_list.append(url)
    
    who_goes_first = True

    return render_to_response('game.html', {'moves': moves, 'url_list': url_list , 'who_goes_first': who_goes_first })


def move( request ):
    '''
    Take URI with game state encoded, calculate the end of game or next move, and render the result.
    '''
    positions = ['c0',
             'c1',
             'c2',
             'c3',
             'c4', 
             'c5', 
             'c6',
             'c7',
             'c8',
             'c9', #indicates if computer goes first
             ]
    moves = {}
    for position in positions:
        moves[position] = 0
    for cell in range(9):
        moves['c' + str(cell)] = int(request.GET.get('c' + str(cell) ))

    game_state = []
    row0 = []
    row1 = []
    row2 = []

    row0.append(moves[positions[0]])
    row0.append(moves[positions[1]])
    row0.append(moves[positions[2]])
    row1.append(moves[positions[3]])
    row1.append(moves[positions[4]])
    row1.append(moves[positions[5]])
    row2.append(moves[positions[6]])
    row2.append(moves[positions[7]])
    row2.append(moves[positions[8]])

    game_state.append(row0)
    game_state.append(row1)
    game_state.append(row2)

    # which move number?
    turn = 0
    for move in moves.values():
        if move != 0:
            turn += 1

    game = TicTacToe()
    game.gui_move(human, turn, game_state)

    try:
        computer_move = game.last_cp_move[0]*3 + game.last_cp_move[1] # transform matrix coordinates to grid_position (row num * 3 + column num)
        moves['c' + str(computer_move)] = -marker
    except AttributeError: # human went last turn
        pass

    if game.win_state == 'win' or game.win_state == 'tie':
        win = True
        return render_to_response('game.html', {'moves': moves, 'win': win })

    url_list = []
    for cell in range(9):
        url ='s?'
        for position in positions:
            # adding substring that corresponds to game state / move
            url += position + '='
            if position[1] == str(cell):
                url += str( marker) # the player's move. 1 or -1
            elif position[1] == str(computer_move):
                url += str( -marker) # the player's move. -1 or 1
            else:
                url += str( moves[position]) #should be 0
                
            if position != 'c9': # add '&' to concatenate next substring
                url += '&'
        url_list.append(url)

    return render_to_response('game.html', {'moves': moves, 'url_list': url_list })

