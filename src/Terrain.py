try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector
import random, sys

sys.setrecursionlimit(10000)


#Constants
WIDTH = 600
HEIGHT = 400

class Terrain:
    def __init__(self, width, height):
	self.walls = []
	self.stack = [(0,0)]
	self.visited = []

	
    def outFrame(self, x, y, width, height):
	if(x<0 or y<0 or x>width or y>height):
	    return True
    def inVisited(self, x, y):
	for i in range(len(self.visited)):
	    if((x, y) == (self.visited[i][0], self.visited[i][1])):
	        return True
    def inStack(self, x, y):
        for i in range(len(self.stack)):
	    if((x, y) == (self.stack[i][0], self.stack[i][1])):
		return True
    def valid(self, aList, width, height):
	newList = []
	for i in range(len(aList)):
	    if self.outFrame(aList[i][0], aList[i][1], width, height):
		continue
	    if self.inVisited(aList[i][0], aList[i][1]):
		continue
	    if self.inStack(aList[i][0], aList[i][1]):
		continue
	    newList.append((aList[i][0], aList[i][1]))	
	return newList
		
    def genMaze(self, width, height, x, y):
	while self.stack:
	    pointer = self.stack[-1]
	    self.walls.append(Vector(pointer[0], pointer[1]))
	    #Create list of valid negibours
	    neigh = [(pointer[0]+10, pointer[1]), (pointer[0]-10, pointer[1]), (pointer[0], pointer[1]+10), (pointer[0], pointer[1]-10)]
	    validNeigh = self.valid(neigh, width, height)
	    random.shuffle(validNeigh)
	    if(len(validNeigh)==0):
		self.visited.append((pointer[0],pointer[1]))
		del self.stack[-1]
	    else:
	        self.stack.append((validNeigh[0][0], validNeigh[0][1]))
				
    def getWalls(self):
	return self.walls
	
    def drawWalls(self, canvas):
	for i in range(len(self.walls)):
	    if (i == len(self.walls)-1):
	        canvas.draw_line(self.walls[i].getP(), self.walls[len(self.walls)-1].getP(), 1, 'Red')
	    else:
		canvas.draw_line(self.walls[i].getP(), self.walls[i+1].getP(), 1, 'Red')

t1 = Terrain(WIDTH, HEIGHT)
t1.genMaze(WIDTH, HEIGHT, 0, 0)

test = t1.getWalls()

def draw(canvas):
    t1.drawWalls(canvas)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", WIDTH, HEIGHT)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
