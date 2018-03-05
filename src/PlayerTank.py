from Vector import Vector
from Line import *
from Projectile import Projectile
import math
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class PlayerTank:
    
    def __init__(self, pos):
        self.rotation = 0
        self.width = 20
        self.height = 20
        self.turret = PlayerTurret(pos)
        self.pos = pos
        self.health = 100.0
        
        self.velocity = Vector(0,0)

        self.generator = Vector(-self.width, -self.height)
        self.projectileSpeed = 10
        self.mousePos = (0,0)
        self.cursor = simplegui.load_image('http://weclipart.com/gimg/19457DF12FD54154/1024px-Crosshairs_Red.svg.png')
        self.readyToFire = True
        self.counter = 120
        self.trackCount = 0
        self.trackMarks = []

    def shoot(self, clickedPos):
        if(not self.readyToFire):
            return
        targetVel = (Vector(clickedPos[0], clickedPos[1])-self.pos.copy()).normalize()
        shot = Projectile(self.pos, targetVel, self.projectileSpeed)
        self.readyToFire = False
        self.counter = 0
        return shot

    def terminalVelocity(self):
        return (math.fabs(self.velocity.length()) >= 1.4)

    def updateVelocityForwards(self):
        if(not self.terminalVelocity()):
            # the velocity added must be rotated to ensure it is in the correct direction
            self.velocity.add(Vector(0,-0.7).rotate(self.rotation))
            self.trackCount += 1
    
    def updateVelocityBackwards(self):
        if(not self.terminalVelocity()):    
            # the velocity added must be rotated to ensure it is in the correct direction
            self.velocity.add(Vector(0,0.7).rotate(self.rotation))
            self.trackCount += 1

    def updateRotationRight(self):
        self.generator.rotate(-1)
        self.rotation -= 1
    
    def updateRotationLeft(self):
        self.generator.rotate(1)
        self.rotation += 1

    def update(self, forwards, backwards, left, right, mousePos):
        if(forwards):
            self.updateVelocityForwards()
        if(backwards):
            self.updateVelocityBackwards()
        if(left):
            self.updateRotationRight()
        if(right):
            self.updateRotationLeft()
        if(not self.readyToFire and self.counter < 120):
            self.counter += 1
        else:
            self.readyToFire = True
        self.pos.add(self.velocity)
        self.turret.setPos(self.pos)
        self.velocity.multiply(0.85)
        self.mousePos = mousePos
        # For representing the front of the tank
        gen = self.generator.copy()
        # Tank is a square primitive, we need the vertices
        self.mesh = list()
        for i in range(4):
            self.mesh.append((self.pos + gen).getP())
            gen.rotate(90)
        self.turret.update(mousePos)
        if(self.trackCount % 3 == 0):
            self.updateTrackMarks(self.generator.copy(),self.mesh[2], self.mesh[3])
   
    def updateTrackMarks(self, gen, leftVectorPos, rightVectorPos):
        gen.rotate(135).divide(4)
        left = Vector(leftVectorPos[0], leftVectorPos[1])
        print(str(left))
        right = Vector(rightVectorPos[0], rightVectorPos[1])
        print(str(right))
        #self.trackMarks.append((left.getP(),right.getP()))
        self.trackMarks.append((Line(
            left, left - gen),
            Line(right, right + gen)))
    
    def drawTrackMarks(self, canvas):
        
        for trackMark1, trackMark2 in self.trackMarks:
            #canvas.draw_point(trackMark1, 'White')
            #canvas.draw_point(trackMark2, 'White')
        #canvas.draw_circle(trackMark1,3,1,'Yellow','Yellow')
        #canvas.draw_circle(trackMark2,3,1,'Red','Red')

        #canvas.draw_text(str(trackMark1), (1,8), 18, 'Yellow',font_face='serif', _font_size_coef=0.75)
        #canvas.draw_text(str(trackMark2), (1,20), 18, 'Red', font_face='serif', _font_size_coef=0.75)
            trackMark1.draw(canvas)
            trackMark2.draw(canvas)

    def draw(self, canvas):
        self.drawTrackMarks(canvas)
        canvas.draw_polygon(self.mesh,3,'#2A2E12','#4B5320') 
        # draw player health
        canvas.draw_line(
                (self.pos.x - (self.width/2), self.pos.y + (self.height/2) + 20), 
                (self.pos.x + (self.width/2), self.pos.y + (self.height/2) + 20), 3, 'Red')
        canvas.draw_line(
                (self.pos.x - (self.width/2), self.pos.y + (self.height/2) + 20), 
                (self.pos.x - (self.width/2) + ((self.health/100)*self.width), self.pos.y + (self.height/2) + 20), 3, 'Green')
        # draw shot trajectory
        aimingLine = DottedLine(self.pos, Vector(self.mousePos[0], self.mousePos[1])).draw(canvas)

        # draw cursor image
        canvas.draw_image(self.cursor, (self.cursor.get_width()/2, self.cursor.get_height()/2), 
                (self.cursor.get_width(), self.cursor.get_height()), self.mousePos, (20, 20))
        self.turret.draw(canvas)
        self.drawReloadStatus(canvas, self.mousePos, 20)
        #canvas.draw_line((self.pos.x, self.pos.y),(self.pos.x + self.generator.x, self.pos.y + self.generator.y), 3, 'Blue')
    
    # draws the status of the reload as a proportion in a circle
    def drawReloadStatus(self, canvas, mousePos, radius):
        # get the counter as a proportion of 360
        angle = (self.counter/120) * 360
        for i in range(int(angle)):
            canvas.draw_point((mousePos[0]+(radius*math.cos(math.radians(i))),
                mousePos[1]+(radius*math.sin(math.radians(i)))), 'Green')

class PlayerTurret:
    
    def __init__(self, pos):
        self.width = 10
        self.height = 10
        self.pos = pos
        self.rotation = 0
        self.sides = 4
        self.generator = Vector(-self.width, -self.height)
    
    def setPos(self, pos):
        self.pos = pos

    def getRotation(self):
        return self.rotation

    def updateRotation(self, newPos):
        xLength = newPos[0] - self.pos.x
        yLength = newPos[1] - self.pos.y
        # theta = tan^-1(opp/adj) SOHCAHTOA :^)
        angle = math.degrees(math.atan2(yLength,xLength))
        difference = angle - self.rotation
        self.rotation += difference
        self.generator.rotate(difference)
	
    def update(self, mousePos):
        self.updateRotation(mousePos)
        gen = self.generator.copy()
        #  is a square primitive, we need the vertices
        self.mesh = list() 
        for i in range(self.sides):
            self.mesh.append((self.pos + gen).getP())
            gen.rotate(360/self.sides)
    
    def draw(self, canvas):
        canvas.draw_polygon(self.mesh,3,'#2A2E12','#4B5320')  
        line = Line(self.pos, self.pos + self.generator.copy().rotate(135), '#2A2E12')
        line.draw(canvas)
