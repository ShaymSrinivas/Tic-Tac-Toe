from django.shortcuts import render_to_response
#import tictactoe

marker = 1 ##TODO: let human choose wether to go first / be x or o. Right now, human = x = 1.

def index( request ):
    #game = TicTacToe()
    #print 'game', game
    positions = ['c0',
             'c1',
             'c2',
             'c3',
             'c4', 
             'c5', 
             'c6',
             'c7',
             'c8',
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
                
            if position != 'c8': # add '&' to concatenate next substring
                url += '&'
        url_list.append(url)
        print 'url_list', url_list

    return render_to_response('game.html', {'moves': moves, 'url_list': url_list })


def move( request ):
    positions = ['c0',
             'c1',
             'c2',
             'c3',
             'c4', 
             'c5', 
             'c6',
             'c7',
             'c8',
             ]
    moves = {}
    for position in positions:
        moves[position] = 0
    # print 'request.GET', request.GET
    # print 'request.GET.get', request.GET.get
    for cell in range(9):
        moves['c' + str(cell)] = int(request.GET.get('c' + str(cell) ))
    # {'c8': 1, 'c3': 0, 'c2': 0, 'c1': 0, 'c0': 1, 'c7': 0, 'c6': 0, 'c5': 0, 'c4': 0}
    game_state = []
    row0 = []
    row1 = []
    row2 = []
    print 'game_state', game_state
    print 'moves[positions[0]]', [moves[positions[0]]]
    row0.append(moves[positions[0]])
    row0.append(moves[positions[1]])
    row0.append(moves[positions[2]])
    print 'row0 = ', row0
    row1.append(moves[positions[3]])
    row1.append(moves[positions[4]])
    row1.append(moves[positions[5]])
    row2.append(moves[positions[6]])
    row2.append(moves[positions[7]])
    row2.append(moves[positions[8]])
    game_state.append(row0)
    game_state.append(row1)
    game_state.append(row2)
    print 'game_state', game_state

    print request.GET.get('c1')
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
                
            if position != 'c8': # add '&' to concatenate next substring
                url += '&'
        url_list.append(url)
        print 'url_list', url_list

    return render_to_response('game.html', {'moves': moves, 'url_list': url_list })

