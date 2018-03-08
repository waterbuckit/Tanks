from Vector import Vector
from Line import Line
import math
import copy

class EnemyTank:

    def __init__(self, pos):
        self.rotation = 0
        self.width = 20
        self.height = 20
        self.turret = EnemyTurret(pos)
        self.pos = pos
        self.health = 100.0
        self.velocity = Vector(0,0)
        
        self.boundingCircleRadius = self.width * 1.414

        self.generator = Vector(-self.width, -self.height)
        self.projectileSpeed = 7
        self.readyToFire = True
        self.interval = 120
        self.reloadCounter = self.interval
        self.trackCount = 0
        self.trackMarks = []
    
    def shoot(self, enemyPos):
        pass
   
    def recoil(self, shot):
        vel = (shot.vel.copy().normalize())*-1
        self.velocity.add(vel)
   
    def update(self):
        self.turret.update()
        # For representing the front of the tank
        gen = self.generator.copy()
        # Tank is a square primitive, we need the vertices
        self.mesh = list()
        for i in range(4):
            self.mesh.append((self.pos + gen).getP())
            gen.rotate(90)
        if(self.trackCount % 3 == 0):
            self.updateTrackMarks(self.generator.copy(),self.mesh[2], self.mesh[3])

    def getPosAndRadius(self):
        return (self.pos.getP(), self.boundingCircleRadius)

    def decreaseHealth(self, projType):
        if(projType == "shell"):
            self.health -= 30
        else:
            self.health -= 3

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
                trackMark1.decreaseAlpha()
                trackMark2.decreaseAlpha()

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
        # draw the collision circle
        canvas.draw_circle(self.pos.getP(), self.boundingCircleRadius, 1, 'Red')
        self.turret.draw(canvas)

class EnemyTurret:

    def __init__(self, pos):
        self.width = 10
        self.height = 10
        self.pos = pos
        self.rotation = 0
        self.sides = 4
        self.generator = Vector(-self.width, -self.height)

    def updateRotation(self, newPos):
        pass

    def update(self):
        #self.updateRotation(newPos)
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