from Vector import Vector
from Line import *
from Projectile import Projectile
import math
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import copy
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
        self.projectileSpeed = 7
        self.mousePos = (0,0)
        self.cursor = simplegui.load_image('https://i.imgur.com/GYXjv5a.png')
        self.readyToFire = True
        self.interval = 120
        self.counter = self.interval
        self.trackCount = 0
        self.trackMarks = []

    def shoot(self, clickedPos):
        clickedVel = Vector(clickedPos[0], clickedPos[1])
        if(not self.readyToFire) or (self.pos - clickedVel).length() < self.generator.length():
            return
        targetVel = (clickedVel-self.pos.copy()).normalize()
        shot = Projectile(self.pos, targetVel, self.projectileSpeed, (self.pos-clickedVel).length())
        self.readyToFire = False
        self.counter = 0
        self.recoil(shot)
        return shot

    #May or may not use
    def shootMg(self, clickedPos):
        if self.counter % 10 == 0:
            targetVel = (Vector(clickedPos[0], clickedPos[1])-self.pos.copy()).normalize()
            shot = Projectile(self.pos, targetVel, self.projectileSpeed*2, (self.pos-Vector(clickedPos[0], clickedPos[1])).length(), False, 2)
            return shot
        return

    def recoil(self, shot):
        vel = (shot.vel.copy().normalize())*-1
        self.velocity.add(vel)

    def terminalVelocity(self):
        return (math.fabs(self.velocity.length()) >= 1.4)

    def updateVelocityForwards(self):
        if(not self.terminalVelocity()):
            # the velocity added must be rotated to ensure it is in the correct direction
            self.velocity.add(Vector(0,-0.7).rotate(self.rotation))
            self.trackCount += 1
            self.trackCount %= 3
    
    def updateVelocityBackwards(self):
        if(not self.terminalVelocity()):    
            # the velocity added must be rotated to ensure it is in the correct direction
            self.velocity.add(Vector(0,0.7).rotate(self.rotation))
            self.trackCount += 1
            self.trackCount %= 3

    def updateRotationRight(self):
        self.generator.rotate(-1)
        self.rotation -= 1
    
    def updateRotationLeft(self):
        self.generator.rotate(1)
        self.rotation += 1

    def update(self, forwards, backwards, left, right, mousePos):
        self.counter += 1
        if(forwards):
            self.updateVelocityForwards()
        if(backwards):
            self.updateVelocityBackwards()
        if(left):
            self.updateRotationRight()
        if(right):
            self.updateRotationLeft()
        if(self.readyToFire or not self.counter < self.interval):
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
        right = Vector(rightVectorPos[0], rightVectorPos[1])
        self.trackMarks.append((Line(
            left, left - gen),
            Line(right, right + gen)))
        trackMarksCopy = copy.copy(self.trackMarks)
        if(not len(self.trackMarks) == 0):
            for trackMark1, trackMark2 in trackMarksCopy:
                if(trackMark1.alpha <= 0 or trackMark2.alpha <= 0):
                    self.trackMarks.remove((trackMark1,trackMark2))
                    continue
                trackMark1.increaseAlpha()
                trackMark2.increaseAlpha()
    
    def drawTrackMarks(self, canvas):
        
        for trackMark1, trackMark2 in self.trackMarks:
            trackMark1.draw(canvas)
            trackMark2.draw(canvas)

    def draw(self, canvas):
        self.drawTrackMarks(canvas)
        canvas.draw_polygon(self.mesh,3,'White','Black') 
        # draw player health
        canvas.draw_line(
                (self.pos.x - (self.width/2), self.pos.y + (self.height/2) + 25), 
                (self.pos.x + (self.width/2), self.pos.y + (self.height/2) + 25), 3, 'Red')
        canvas.draw_line(
                (self.pos.x - (self.width/2), self.pos.y + (self.height/2) + 25), 
                (self.pos.x - (self.width/2) + ((self.health/100)*self.width), self.pos.y + (self.height/2) + 25), 3, 'Green')
        # draw shot trajectory
        aimingLine = DottedLine(self.pos, Vector(self.mousePos[0], self.mousePos[1])).draw(canvas)

        # draw cursor image
        canvas.draw_image(self.cursor, (self.cursor.get_width()/2, self.cursor.get_height()/2), 
                (self.cursor.get_width(), self.cursor.get_height()), self.mousePos, (20, 20))
        self.turret.draw(canvas)
        self.drawReloadStatus(canvas, self.mousePos, 9)
    
    # draws the status of the reload as a proportion in a circle
    def drawReloadStatus(self, canvas, mousePos, radius):
        # get the counter as a proportion of 360
        angle = (self.counter/self.interval) * 360
        for i in range(int(angle)):
            canvas.draw_point((mousePos[0]+(radius*math.cos(math.radians(i))),
                mousePos[1]+(radius*math.sin(math.radians(i)))), 'White')

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
        canvas.draw_polygon(self.mesh,3,'White','Black')  
        line = Line(self.pos, self.pos + self.generator.copy().rotate(135))
        line.draw(canvas)
