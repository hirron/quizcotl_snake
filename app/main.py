import bottle
import os
import random
import math
import copy

def direction(from_cell, to_cell):
    dx = to_cell[0] - from_cell[0]
    dy = to_cell[1] - from_cell[1]

    if dx == 1:
        return 'east'
    elif dx == -1:
        return 'west'
    elif dy == -1:
        return 'north'
    elif dy == 1:
        return 'south'

def distance(p, q):
    dx = abs(p[0] - q[0])
    dy = abs(p[1] - q[1])
    return dx + dy;

def closest(items, start):
    closest_item = None
    closest_distance = 10000

    # TODO: use builtin min for speed up
    for item in items:
        item_distance = distance(start, item)
        if item_distance < closest_distance:
            closest_item = item
            closest_distance = item_distance

    return closest_item



@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
	directions = ['up', 'down', 'left', 'right']	
	data = bottle.request.json
	foodList = data['food'].get('data')
	snakeList = data['snakes'].get('data')
	youList = data['you'].get('body').get('data')
	
	#print("my location")
	#print(youList)
	#print('other snake location')
	#print(snakeList)
	#print('food location')
	#print(foodList)
	print('\n')

    # TODO: Do things with data
    
   
	if len(foodList) > 0:
		moveTo=direction((youList[0].get('x'),youList[0].get('y')),(foodList[0].get('x'),foodList[0].get('y')))
		print("decided to move:" + moveTo)
	else:
		print("no food")
		moveTo = 'north'
	
	return {
		'move': moveTo,
		'taunt': 'The sun darkens!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
