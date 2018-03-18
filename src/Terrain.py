try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector
from Line import Line
from ItemPickUp import ItemPickUp
import random, sys

sys.setrecursionlimit(10000)

class Terrain:
    def __init__(self, width, height, game):
        self.game = game
        self.walls = []
        self.pathSize = 125
        self.stack = [(self.pathSize,self.pathSize)]
        self.visited = []
        self.lines = []
        self.width = width
        self.height = height
        self.pickupItems =[]
        self.itemRadius = 10

    def outFrame(self, x, y, width, height):
        if x < 0+self.pathSize or y < 0+self.pathSize or x > width-self.pathSize or y > height-self.pathSize:
            return True

    def inVisited(self, x, y):
        for i in range(len(self.visited)):
            if (x, y) == (self.visited[i][0], self.visited[i][1]):
                return True

    def inStack(self, x, y):
        for i in range(len(self.stack)):
            if (x, y) == (self.stack[i][0], self.stack[i][1]):
                return True
    
    def genRandomPoint(self):
        listOfPoints = []
        #Adds pick up to random coords not on a line
        while len(self.pickupItems) < random.randrange(2,5):
            point = Vector(random.randint(0, 1200), random.randint(0, 800))
            if not(self.inWalls(point)) and not(self.inWallRadius(point)):
                self.pickupItems.append(ItemPickUp(point, self.game))

    def inWallRadius(self, point):
        for line in self.lines:
            if(line.distanceTo(point) <= line.thickness + 25):
                return True
    
    def inWalls(self, point):
        for i in range(len(self.walls)):
            if(point == self.walls[i]):
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

    def genMaze(self, x, y):
        while self.stack:
            pointer = self.stack[-1]
            self.walls.append(Vector(pointer[0], pointer[1]))
            #Create list of valid negibours
            neigh = [(pointer[0]+self.pathSize, pointer[1]),
                    (pointer[0]-self.pathSize, pointer[1]),
                    (pointer[0], pointer[1]+self.pathSize),
                    (pointer[0], pointer[1]-self.pathSize)]
            validNeigh = self.valid(neigh, self.width, self.height)
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
        self.lines.append(Line(Vector(0, 0), Vector(0, self.height)))
        self.lines.append(Line(Vector(0, self.height), Vector(self.width, self.height)))
        self.lines.append(Line(Vector(self.width, self.height), Vector(self.width, 0)))
        self.lines.append(Line(Vector(self.width, 0), Vector(0, 0)))
        self.genRandomPoint()
	
    def drawWalls(self, canvas):
        for line in self.lines:
            line.draw(canvas)
