from Vector import Vector
from Line import Line
from Projectile import Projectile, HomingProjectile
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import copy
import random

class Tank:

    defWidth = 20
    defHeight = 20
    defRadius = defWidth * 1.414

    def __init__(self, pos, game):
        self.game = game
        self.linesRef = game.terrain.lines
        self.rotation = 0
        self.width = Tank.defWidth
        self.height = Tank.defHeight
        self.pos = pos
        self.health = 100.0
        self.velocity = Vector(0,0)
        self.boundingCircleRadius = Tank.defRadius
        self.generator = Vector(-self.width, -self.height)
        self.turret = Turret(self, pos)
        self.projectileSpeed = 7
        self.readyToFire = True
        self.counter = 0
        self.interval = 120
        self.reloadCounter = self.interval
        self.trackCount = 0
        self.trackMarks = []
    
    def getPosAndRadius(self):
        return self.pos.getP(), self.boundingCircleRadius

    def recoil(self, shot):
        pass

    def terminalVelocity(self):
        return abs(self.velocity.length()) > 1.4

    def updateVelocityForwards(self):
        if(not self.terminalVelocity()):
            self.velocity.add(Vector(0,-0.7).rotate(self.rotation))
            self.trackCount += 1
            self.trackCount %= 6
    
    def updateVelocityBackwards(self):
        if(not self.terminalVelocity()):    
            self.velocity.add(Vector(0,0.7).rotate(self.rotation))
            self.trackCount += 1
            self.trackCount %= 6

    def updateRotationRight(self):
        self.generator.rotate(-1)
        self.rotation -= 1
    
    def updateRotationLeft(self):
        self.generator.rotate(1)
        self.rotation += 1

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

    def newTankPos(terrain, width, height):
        newPos = Vector(random.randrange(Tank.defWidth, width-Tank.defWidth), 
                        random.randrange(Tank.defHeight, height-Tank.defHeight))
        for line in terrain.lines:
            if line.distanceTo(newPos) <= Tank.defRadius+5 + line.thickness:
                return Tank.newTankPos(terrain, width, height)
        return newPos

    def update(self, mousePos):
        if(not self.readyToFire):
            self.reloadCounter += 1
        self.counter += 1
        self.counter %= 100
        if(not self.reloadCounter < self.interval):
            self.readyToFire = True
        self.pos.add(self.velocity)
        self.turret.setPos(self.pos)
        self.velocity.multiply(0.65)
        gen = self.generator.copy()
        self.mesh = list()
        for i in range(4):
            self.mesh.append((self.pos + gen).getP())
            gen.rotate(90)
        self.turret.update(mousePos)
        if(self.trackCount % 6 == 0 and self.velocity.length() > 0.5):
            self.updateTrackMarks(self.generator.copy(),self.mesh[2], self.mesh[3])

    def draw(self, canvas):
        self.drawTrackMarks(canvas)
        canvas.draw_polygon(self.mesh,3,'White','Black')
        canvas.draw_line(
                (self.pos.x - (self.width/2), self.pos.y + (self.height/2) + 25), 
                (self.pos.x + (self.width/2), self.pos.y + (self.height/2) + 25), 3, '#ff180c')
        canvas.draw_line(
                (self.pos.x - (self.width/2), self.pos.y + (self.height/2) + 25), 
                (self.pos.x - (self.width/2) + ((self.health/100)*self.width), self.pos.y + (self.height/2) + 25), 3, '#80ff56')
        self.turret.draw(canvas)

class Turret:

    def __init__(self, base, pos):
        self.base = base
        self.pos = pos
        self.width = 10
        self.height = 10
        self.rotation = 0
        self.sides = 4
        self.generator = Vector(-self.width, -self.height)
        self.projectileSpeed = 6
        self.lOS = False
        self.patrolCount = random.randint(0,360)
        self.aimPos = self.pos.copy()
    def setPos(self, pos):
        self.pos = pos

    def getMuzzlePos(self):
        return self.pos + self.generator.copy().rotate(135) * 2.6

    def updateRotation(self, newPos):
        xLength = newPos.x - self.pos.x
        yLength = newPos.y - self.pos.y
        angle = math.degrees(math.atan2(yLength,xLength))
        difference = angle - self.rotation
        self.rotation += difference
        self.generator.rotate(difference)

    def patrol(self):
        self.updateRotationByDeg()

    def updateRotationByDeg(self):
        self.patrolCount += 1
        self.patrolCount %= 360
        difference = self.patrolCount - self.rotation
        self.rotation += difference
        self.generator.rotate(difference)

    def shoot(self, clickedVel, type):
        if(not self.lOS) : return
        targetVel = (clickedVel-self.getMuzzlePos()).normalize()
        if((not self.base.readyToFire) or (self.pos - clickedVel).length() < self.generator.length()):
            return
        if type == "shell":
            shot = Projectile(self.getMuzzlePos(), targetVel, self.projectileSpeed, "shell", (self.pos-clickedVel).length())
            self.base.recoil(shot)
        elif type == "homing":
            shot = HomingProjectile(self.getMuzzlePos(), targetVel)
        self.base.readyToFire = False
        self.base.reloadCounter = 0
        return shot
     
    def shootMg(self, clickedVel):
        if self.base.counter % 10 == 0:
            targetVel = (clickedVel - self.getMuzzlePos()).normalize()
            shot = Projectile(self.getMuzzlePos(), targetVel, self.projectileSpeed*2, "mg",(self.getMuzzlePos()-clickedVel).length(), False, 2,)
            return shot
        return

    def aim(self, target):
        a = target.velocity.x**2 + target.velocity.y**2 - self.projectileSpeed**2
        b = (target.velocity.x * (target.pos.x - self.pos.x) + target.velocity.y * (target.pos.y - self.pos.y))
        c = (target.pos.x - self.pos.x)**2 + (target.pos.y - self.pos.y)**2
        discriminant = b**2 - 6 * a * c
        t = (-b - math.sqrt(math.fabs(discriminant))) / (a*2)
        self.aimPos = Vector(t*target.velocity.x+target.pos.x, t*target.velocity.y + target.pos.y)
        if self.aimPos.x % 1200 != self.aimPos.x or self.aimPos.y % 800 != self.aimPos.y:
            return target.pos
        return self.aimPos
 
    def findIntersection(self, playerPos, pA, pB):
        s10_x = playerPos.x - self.pos.x
        s10_y = playerPos.y - self.pos.y
        s32_x = pB.x - pA.x
        s32_y = pB.y - pA.y
        denom = s10_x * s32_y - s32_x * s10_y
        if denom == 0 : return None # collinear
        denom_is_positive = denom > 0
        s02_x = self.pos.x - pA.x
        s02_y = self.pos.y - pA.y
        s_numer = s10_x * s02_y - s10_y * s02_x
        if (s_numer < 0) == denom_is_positive : return None # no collision
        t_numer = s32_x * s02_y - s32_y * s02_x
        if (t_numer < 0) == denom_is_positive : return None # no collision
        if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None # no collision
        t = t_numer / denom

        intersectionPoint = (self.pos.x + (t * s10_x), self.pos.y + (t * s10_y))
        return intersectionPoint

    def update(self, target):  
        for line in self.base.linesRef:
            findIntersectionPointRes = self.findIntersection(target.pos, line.pA, line.pB)
            if(findIntersectionPointRes is not None):
                self.lOS = False
                break
            else:
                self.lOS = True
        if(self.lOS):
            self.updateRotation(self.aim(target))
        else:
            self.patrol()
        gen = self.generator.copy()
        self.mesh = list() 
        for i in range(self.sides):
            self.mesh.append((self.pos + gen).getP())
            gen.rotate(360/self.sides)

    def draw(self, canvas):
        canvas.draw_polygon(self.mesh,3,'White','Black')
        line = Line(self.pos, self.getMuzzlePos())
        line.draw(canvas)
