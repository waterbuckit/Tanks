try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vectors import Vector
import random



class Terrain:
    def __init__(self, width, height, terrWidth, terrHeight):
        self.terrPos = []
        self.freePos = []
        self.terrWidth = terrWidth
        self.terrHeight = terrHeight
        self.spaces = ((width//self.terrWidth)*(height//self.terrHeight))//2
    
    #Creates a border and adds used spaces to a list
    def createBorder(self,canvas, width, height):
        img = simplegui.load_image("https://i.ytimg.com/vi/62d17RtgVU8/maxresdefault.jpg")
        for x in range(0, width):
            for y in range(0, height):
                if(x == 0)or(y == 0):
                    pos = Vector(x, y)
                    oppPos = Vector((width-x), (height-y))
                    self.terrPos.append(pos)
                    self.terrPos.append(oppPos)
        for i in range(len(self.terrPos)):		
            canvas.draw_image(img,(1280//2, 720//2), (1280,720), ((self.terrPos[i].getP()[0]),(self.terrPos[i].getP()[1])),(10,10))
    
    #Checks if a space is valid for placement    
    def valid(self, x, y, width, height):
        for i in range(len(self.terrPos)):
            if (self.terrPos[i] == Vector(x,y)):
                return True
            if( x<0 or y<0 or x>=width or y>=height ):
                return True
        return False
    
    def	findFree(self, x, y, width, height):
        if self.valid(x, y, width, height):
            return
        if not self.valid(x, y, width, height):
            self.freePos.append(Vector(x,y))
            self.findFree(x-1, y, width, height)
            self.findFree(x+1, y, width, height)
            self.findFree(x, y-1, width, height)
            self.findFree(x, y+1, width, height)     
    
        
    def getTerrPos(self):
        return self.terrPos
    
    def getFreePos(self):
        return self.freePos
