try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vectors import Vector
import random



class Terrain:
	def __init__(self, width, height, terrWidth, terrHeight):
		self.terrPos = []
		self.terrWidth = terrWidth
		self.terrHeight = terrHeight
		self.spaces = ((width//self.terrWidth)*(height//self.terrHeight))//2
    
    #Creates a border and adds used spaces to a list
	def genBorder(self, width, height):
		for x in range(0, width):
			for y in range(0, height):
				if((x == 0)or(y == 0))and((x%5==0)or(y%5==0)):
					pos = Vector(x, y)
					oppPos = Vector((width-x), (height-y))
					self.terrPos.append(pos)
					self.terrPos.append(oppPos)
	
	#Draws border from list of generated points
	def drawAll(self, canvas):
		img = simplegui.load_image("https://i.ytimg.com/vi/62d17RtgVU8/maxresdefault.jpg")
		for i in range(len(self.terrPos)):		
			canvas.draw_image(img,(1280//2, 720//2), (1280,720), ((self.terrPos[i].getP()[0]),(self.terrPos[i].getP()[1])),(10,10))
    
    #Checks if a space is valid for placement    
	def valid(self, x, y, width, height):
		for i in range(len(self.terrPos)):
			if(self.terrPos[i].getP() == (x, y)):
				return True
			if not (((x%5==0)and(y%5!=0))or((x%5!=0)and(y%5==0))):
				return True
		if(x<0 or y<0 or x>=width or y>=height ):
			return True
		return False
	
					
		
	def drawMaze(self,canvas, width, height, x, y):
			if not(self.valid(x, y, width, height)):
				self.terrPos.append(Vector(x, y))
				xOry = random.randint(0,1) #Choose which coord to add 1 to
				aOrs = random.randint(0,1) # Choose if we add or subtract
				if(aOrs == 0):
					if(xOry == 0):
						self.drawMaze(canvas, width, height, x+1, y)
					else:
						self.drawMaze(canvas, width, height, x, y+1)
				else:
					if(xOry == 0):
						self.drawMaze(canvas, width, height, x-1, y)
					else:
						self.drawMaze(canvas, width, height, x, y-1)

    
        
	def getTerrPos(self):
		return self.terrPos
    
