try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector
from Line import Line
import random, sys
from PlayerTank import PlayerTank

sys.setrecursionlimit(10000)

class Terrain:
	def __init__(self, width, height):
		self.walls = []
		self.pathSize = 100
		self.stack = [(self.pathSize,self.pathSize)]
		self.visited = []
		self.lines = []
		self.width = width
		self.height = height
		self.pickupItems =[]

		self.genRandomPoint()


	def genRandomPoint(self):
		listOfPoints = []
		#Adds pick up to random coords not on a line
		for i in range(0, 5):
			point = Vector(random.randint(0, 1200), random.randint(0, 800))
			if not(self.inWalls(point)) and not(self.inWallRadius(point)):
				self.pickupItems.append(point)
				print(self.pickupItems)
				



	def drawItemPickUp(self, canvas, player):
		LINE_WIDTH = 2


		self.pickupItems = player.pickUpItem(self.pickupItems)
		for item in self.pickupItems:
			canvas.draw_circle(item.getP(), 10, LINE_WIDTH, 'Red', 'Red')


	def inWallRadius(self, point):
		for line in self.lines:
			if(line.distanceTo(point)< line.thickness + 10*2 + 30):
				return True




	def outFrame(self, x, y, width, height):
		if x < 0+self.pathSize or y < 0+self.pathSize or x > width-self.pathSize or y > height-self.pathSize:
			return True

	def inVisited(self, x, y):
		for i in range(len(self.visited)):
			if (x, y) == (self.visited[i][0], self.visited[i][1]):
				return True
	def inWalls(self, point):
		for i in range(len(self.walls)):
			if(point == self.walls[i]):
				return True

	def inStack(self, x, y):
		for i in range(len(self.stack)):
			if (x, y) == (self.stack[i][0], self.stack[i][1]):
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
			neigh = [(pointer[0]+self.pathSize, pointer[1]),
					(pointer[0]-self.pathSize, pointer[1]),
					(pointer[0], pointer[1]+self.pathSize),
					(pointer[0], pointer[1]-self.pathSize)]
			validNeigh = self.valid(neigh, width, height)
			random.shuffle(validNeigh)
			if(len(validNeigh)==0):
				self.visited.append((pointer[0],pointer[1]))
				del self.stack[-1]
			else:
				self.stack.append((validNeigh[0][0], validNeigh[0][1]))
		self.getLines()


	def getWalls(self):
		return self.walls

	def getLines(self):
		for i in range(len(self.walls)-1):
			self.lines.append(Line(Vector(self.walls[i].x, self.walls[i].y), Vector(self.walls[i+1].x,
				self.walls[i+1].y)))
		self.lines.append(Line(Vector(3,3), Vector(3, self.height-3)))
		self.lines.append(Line(Vector(3,self.height-3), Vector(self.width-3, self.height-3)))
		self.lines.append(Line(Vector(self.width-3, self.height-3), Vector(self.width-3, 3)))
		self.lines.append(Line(Vector(self.width-3, 3), Vector(3, 3)))

	
	def drawWalls(self, canvas):
		for line in self.lines:
			line.draw(canvas)



