from Vector import Vector
from Line import Line
from Projectile import Projectile
import math
import copy
import cmath

class EnemyTank:

    def __init__(self, pos):
        self.rotation = 0
        self.width = 20
        self.height = 20
        self.turret = EnemyTurret(self, pos)
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
    
    def recoil(self, shot):
        vel = (shot.vel.copy().normalize())*-1
        self.velocity.add(vel)
   
    def update(self, target):
        self.turret.update(target)
        gen = self.generator.copy()
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
        elif(projType == "homing"):
            self.health -= 50
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

    def __init__(self, base, pos):
        self.base = base
        self.width = 10
        self.height = 10
        self.pos = pos
        self.rotation = 0
        self.sides = 4
        self.generator = Vector(-self.width, -self.height)
        self.projectileSpeed = 7
        self.aimPos = self.generator

    def updateRotation(self, newPos):
        xLength = newPos.x - self.pos.x
        yLength = newPos.y - self.pos.y
        angle = math.degrees(math.atan2(yLength, xLength))
        difference = angle - self.rotation
        self.rotation += difference
        self.generator.rotate(difference)

    def getMuzzlePos(self):
        return self.pos + self.generator.copy().rotate(135) * 2.2

    def shoot(self):
        target = self.aimPos
        targetVel = (target - self.getMuzzlePos()).normalize()
        shot = Projectile(self.getMuzzlePos(), targetVel, self.projectileSpeed, "shell", (self.pos-target).length()) 
        self.base.recoil(shot)
        return shot
    
    def aim(self, target):
        a = target.velocity.x**2 + target.velocity.y**2 - self.projectileSpeed**2
        b = (target.velocity.x * (target.pos.x - self.pos.x) + target.velocity.y * (target.pos.y - self.pos.y))
        c = (target.pos.x - self.pos.x)**2 + (target.pos.y - self.pos.y)**2
        discriminant = b**2 - 4 * a * c
        t = (-b - math.sqrt(discriminant)) / (a*2)
        self.aimPos = Vector(t*target.velocity.x+target.pos.x, t*target.velocity.y + target.pos.y)
        self.updateRotation(self.aimPos)

    def update(self, target):
        self.aim(target)
        gen = self.generator.copy()
        self.mesh = list() 
        for i in range(self.sides):
            self.mesh.append((self.pos + gen).getP())
            gen.rotate(360/self.sides)

    def draw(self, canvas):
        canvas.draw_polygon(self.mesh,3,'White','Black')  
        line = Line(self.pos, self.getMuzzlePos())
        line.draw(canvas)
       
