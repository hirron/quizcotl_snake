import bottle
import os
import random
import math
import copy

#Global Variables
NumTries = 3
FoodVal = 10
HeadNodeVal = 5
SnakeNodeVal = -5
############



def direction(from_cell, to_cell):
	print("Moving from "+str(from_cell) + "to " + str(to_cell))
	dx = to_cell[0] - from_cell[0]
	dy = to_cell[1] - from_cell[1]
	
	
	if dx > 0:
		return 'right'
	elif dx < 0:
		return 'left'
	elif dy <  0:
		return 'up'
	elif dy > 0:
		return 'down'

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

def getPointList(data):
	pointList = []
	for point in data:
		newPoint = (point.get('x'), point.get('y'))
		pointList.append(newPoint)
	
	return pointList
	
def maxIndex(arr):
		max = -1000
		x = 0
		retInd = 0
		
		for val in arr:
			if val > max:
				max = val
				retInd = x
		x = x+1
		
		return retInd

	

def getBestValue(grid, head):
	vals =[grid[head[0]-1][head[1]], grid[head[0]+1][head[1]], grid[head[0]][head[1]-1], grid[head[0]][head[1]+1]]
	
	if(head[0] == (len(grid)-1)):
		vals[1] = -100000
		
	if(head[1] == (len(grid)-1)):
		vals[3] = -100000
		
	if(head[0] == 0):
		vals[0] = -100000
	
	if(head[1] == 0):
		vals[2] = -100000

	highestIndex = maxIndex(vals)

	if highestIndex == 0:
		return (head[0]-1,head[1])
	if highestIndex == 1:
		return (head[0]+1, head[1])
	if highestIndex == 2:
		return(head[0],head[1]-1)
	if highestIndex == 3:
		return(head[0],head[1]+1)

def handleSnakeBodies(grid, data):
	for snakeData in data:
		for body in snakeData:
			bodyNodes = getPointList(body)
			for Node in bodyNodes:
				grid[node[0]][node[1]] = SnakeNodeVal
					
	
def updateGrid(Grid):
	n = 0
	while n < NumTries:
		for row in grid:
			for column in row:
				Grid[row][column] = Grid[row][column] + (1/2)*(Grid[row-1][column]+Grid[row+1][column]+Grid[row][column+1]+Grid[row][column-1])	
		n = n+1
	return Grid


@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
	targetPoint = None
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

	
targetPoint = None
@bottle.post('/move')
def move():
	
	directions = ['up', 'down', 'left', 'right']	
	data = bottle.request.json
	grid = [[0 for col in xrange(data['width'])] for row in xrange(data['width'])]
	
	foodList = getPointList(data['food'].get('data'))
	
	for point in foodList:
		grid[point[0]][point[1]] = FoodVal
	
	print(grid)
	
	snakeList = data['snakes'].get('data')
	youList = data['you'].get('body').get('data')
	
	
	head = (youList[0].get('x'),youList[0].get('y'))

	if targetPoint == None:
		targetPoint = closest(foodList, head)
	
	if targetPoint not in foodList:
		targetPoint = closest(foodList, head)
	
   
	if len(foodList) > 0:
		moveTo = direction(head,targetPoint)

	
	print("decided to move:" + moveTo)

	updateGrid(Grid)
	#grid[(youList[1].get('x')][youList[1].get('y')] = -1000000
	#targetPoint = GetBestValue(Grid, head)
	moveTo = direction(head,targetPoint)

	
	print()
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
