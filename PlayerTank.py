from Vector import Vector
from Line import Line
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
        self.projectileSpeed = 3
        #self.mesh = Mesh(self.width, self.height, self.pos)
        
    def shoot(self, clickedPos):
        targetVel = (Vector(clickedPos[0], clickedPos[1])-self.pos.copy()).normalize()
        shot = Projectile(self.pos, targetVel, self.projectileSpeed)
        return shot

    def terminalVelocity(self):
        return (self.velocity.length() >= 1.5)

    def updateVelocityForwards(self):
        if(not self.terminalVelocity()):
            # the velocity added must be rotated to ensure it is in the correct direction
            self.velocity.add(Vector(0,-0.7).rotate(self.rotation))
    
    def updateVelocityBackwards(self):
            # the velocity added must be rotated to ensure it is in the correct direction
            self.velocity.add(Vector(0,0.7).rotate(self.rotation))

    def updateRotationRight(self):
        self.generator.rotate(-1)
        self.rotation -= 1
    
    def updateRotationLeft(self):
        self.generator.rotate(1)
        self.rotation += 1

    def update(self, forwards, backwards, left, right):
        if(forwards):
            self.updateVelocityForwards()
        if(backwards):
            self.updateVelocityBackwards()
        if(left):
            self.updateRotationRight()
        if(right):
            self.updateRotationLeft()
        self.pos.add(self.velocity)
        self.turret.setPos(self.pos)
        self.velocity.multiply(0.85)
        # For representing the front of the tank
        gen = self.generator.copy()
        # Tank is a square primitive, we need the vertices
        self.mesh = list() 
        for i in range(4):
            self.mesh.append(self.pos + gen)
            gen.rotate(90)
        # compute the lines
        self.lines = [ Line(self.mesh[i], self.mesh[(i + 1) % len(self.mesh)])
                       for i in range(len(self.mesh)) ]
        self.turret.update()
        #self.frontPoint = Vector(self.pos.x, self.pos.y) + gen
        # For representing the back of the tank
        #gen.rotate(180)
        #self.backPoint = Vector(self.pos.x, self.pos.y) + gen
        #self.mesh.update()
    def draw(self, canvas):
        for line in self.lines:
            line.draw(canvas)
        # draw player health
        canvas.draw_line((self.pos.x - (self.width/2), self.pos.y + (self.height/2) + 20), (self.pos.x + (self.width/2), self.pos.y + (self.height/2) + 20), 3, 'Red')
        canvas.draw_line((self.pos.x - (self.width/2), self.pos.y + (self.height/2) + 20), (self.pos.x + ((self.health/100)*self.width/2), self.pos.y + (self.height/2) + 20), 3, 'Green')
        self.turret.draw(canvas)

        #line = Line(self.pos, self.pos + self.generator)
        #line.draw(canvas)
        #self.mesh.draw(canvas)
        # Temporarily use a line to represent the current rotation
        #canvas.draw_line((self.frontPoint.x, self.frontPoint.y), (self.backPoint.x, self.backPoint.y), 12, 'Red')

class PlayerTurret:
    
    def __init__(self, pos):
        self.width = 10
        self.height = 10
        self.pos = pos
        self.rotation = 0
        self.sides = 4
        self.generator = Vector(-self.width, -self.height)
        # self.mesh = Mesh(self.width, self.height, self.pos)
    
    def setPos(self, pos):
        self.pos = pos

    def getRotation(self):
        return self.rotation
    # this is broken :~;
    def updateRotation(self, clickedPos):
        xLength = clickedPos[0] - self.pos.x
        yLength = clickedPos[1] - self.pos.y
        # theta = tan^-1(opp/adj) SOHCAHTOA :^)
        angle = math.degrees(math.atan(yLength/xLength))
        difference = angle - self.rotation
        self.rotation += difference
        self.generator.rotate(difference)
	
    def update(self):
        gen = self.generator.copy()
        #  is a square primitive, we need the vertices
        self.mesh = list() 
        for i in range(self.sides):
            self.mesh.append(self.pos + gen)
            gen.rotate(360/self.sides)
	# compute the lines
        self.lines = [ Line(self.mesh[i], self.mesh[(i + 1) % len(self.mesh)])
                       for i in range(len(self.mesh)) ]
    
    def draw(self, canvas):
        for line in self.lines:
            line.draw(canvas)
        line = Line(self.pos, self.pos + self.generator)
        line.draw(canvas)
