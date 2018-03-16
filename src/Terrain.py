try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector
from Line import Line
import random, sys

sys.setrecursionlimit(10000)

class Terrain:
    def __init__(self, width, height):
        self.walls = []
        self.pathSize = 125
        self.stack = [(self.pathSize,self.pathSize)]
        self.visited = []
        self.lines = []
        self.width = width
        self.height = height

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
        self.lines.append(Line(Vector(3,3), Vector(3, self.height-3)))
        self.lines.append(Line(Vector(3,self.height-3), Vector(self.width-3, self.height-3)))
        self.lines.append(Line(Vector(self.width-3, self.height-3), Vector(self.width-3, 3)))
        self.lines.append(Line(Vector(self.width-3, 3), Vector(3, 3)))
	
    def drawWalls(self, canvas):
        for line in self.lines:
            line.draw(canvas)
