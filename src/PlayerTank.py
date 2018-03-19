from Line import *
from Tank import *
from ItemPickUp import ItemPickUp
import SimpleGUICS2Pygame.codeskulptor_lib as simpleguiUtils
import math

class PlayerTank(Tank):
   
    shieldSize = Tank.defRadius + 5

    def __init__(self, pos, game):
        Tank.__init__(self, pos, game)
        self.mousePos = (0,0)
        self.cursor = simplegui.load_image('https://i.imgur.com/GYXjv5a.png')
        self.turret = PlayerTurret(self, pos, self)
        self.counter = 100
        self.shieldStatus = 100
        self.shield = Shield(self)
        self.maxHealth = 100
        self.isColliding = False
        self.homingAmmo = 0
    
    def recoil(self, shot):
        vel = shot.vel.copy().normalize()*-2
        self.velocity.add(vel)
    
    def isCollidingWithLine(self, line):
        return (line.distanceTo(self.pos) < line.thickness + self.boundingCircleRadius and
            line.covers(self.pos))

    def isCollidingWithLineTipA(self, line):
        return(line.pA.getDistance(self.pos) < self.boundingCircleRadius + line.pointRadius)
    
    def isCollidingWithLineTipB(self, line):
        return(line.pB.getDistance(self.pos) < self.boundingCircleRadius + line.pointRadius)
    
    def collideTip(self, point):
        normal = point.copy().subtract(self.pos).normalize().negate()
        self.velocity.reflect(normal).multiply(1.9)
        self.pos.add(self.velocity)

    def collide(self, line):
        copy = self.velocity.copy()
        copy.reflect(line.normal)
        if((copy.x < 0 and self.velocity.x > 0) or (copy.x > 0 and self.velocity.x < 0)):
            self.velocity.x *= -1
            self.velocity.multiply(1.9)
            self.pos.x += self.velocity.x
        elif((copy.y < 0 and self.velocity.y > 0) or (copy.y > 0 and self.velocity.y < 0)):
            self.velocity.y *= -1
            self.velocity.multiply(1.9)
            self.pos.y += self.velocity.y

    def decreaseShield(self, projType):
        if(projType == "shell"):
            self.shieldStatus -= 15
            if(self.shieldStatus < 0):
                self.shieldStatus = 0
        elif(projType == "homing"):
            self.health -= 25
        else:
            self.health -= 3

    def pickUpItem(self, item):
        if((self.pos - item.pos).length() <= self.defRadius + ItemPickUp.sizes[2]):
            item.pickupAction(self)
            return True

    def update(self, forwards, backwards, left, right, mousePos):
        if(forwards):
            self.updateVelocityForwards()
        if(backwards):
            self.updateVelocityBackwards()
        if(left):
            self.updateRotationRight()
        if(right):
            self.updateRotationLeft()
        self.mousePos = mousePos
        Tank.update(self, mousePos)
        self.shield.update()

    def draw(self, canvas):
        # draws a the line from the muzzle to the cursor position
        aimingLine = DottedLine(self.pos, Vector(self.mousePos[0], self.mousePos[1])).draw(canvas)
        canvas.draw_image(self.cursor, (self.cursor.get_width()/2, self.cursor.get_height()/2), 
                (self.cursor.get_width(), self.cursor.get_height()), self.mousePos, (20, 20))
        self.drawReloadStatus(canvas, self.mousePos, 9)
        # draw shield status (currently made specific to player tank)
        if(self.shieldStatus > 0):
            self.shield.draw(canvas)
            canvas.draw_line(
                (self.pos.x - (self.width/2), self.pos.y + (self.height/2) + 30), 
                (self.pos.x + (self.width/2), self.pos.y + (self.height/2) + 30), 3, '#032459')
            canvas.draw_line(
                (self.pos.x - (self.width/2), self.pos.y + (self.height/2) + 30), 
                (self.pos.x - (self.width/2) + ((self.shieldStatus/100)*self.width),
                self.pos.y + (self.height/2) + 30), 3, '#8eddff')
        Tank.draw(self, canvas)

    # Draws the circle surrounding the cursor point indicating how "reloaded" the tank is
    def drawReloadStatus(self, canvas, mousePos, radius):
        angle = (self.reloadCounter/self.interval) * 360
        for i in range(int(angle)):
            canvas.draw_point((mousePos[0]+(radius*math.cos(math.radians(i))),
                mousePos[1]+(radius*math.sin(math.radians(i)))), 'White')

class Shield:
    def __init__(self, base):
        self.base = base
        # god knows why I did this retarded naming but laziness prevails
        self.shieldRadius = base.shieldSize
        self.shieldHitmarks = []
    
    def update(self):
        for hitmark in self.shieldHitmarks:
            hitmark.update(self.base.pos)
            if(hitmark.alpha <= 0.05):
                self.shieldHitmarks.remove(hitmark)

    def draw(self, canvas):
        for hitmark in self.shieldHitmarks:
            hitmark.draw(canvas)

    # take the position of the hit and spread the mark around that position(like +- 20 degrees)
    def receiveHit(self, pos):
        xLength = pos.x - self.base.pos.x
        yLength = pos.y - self.base.pos.y
        angle = math.degrees(math.atan2(yLength,xLength))
        for i in range(int(angle - 30),int(angle + 30)):
            self.shieldHitmarks.append(ShieldHitmark(Vector(
                self.base.pos.x + (self.shieldRadius * math.cos(math.radians(i % 360))),
                self.base.pos.y + (self.shieldRadius * math.sin(math.radians(i % 360)))),i%360))

class ShieldHitmark:
    def __init__(self, pos, angle):
        self.pos = pos
        self.angle = angle
        self.alpha = 1.0
        self.brightness = 100
        self.ceiling = 0.94 
        self.colour = simpleguiUtils.hsla(170, 100, 90,self.alpha) 
    
    def draw(self, canvas):
        canvas.draw_circle(self.pos.getP(),3,3,self.colour, self.colour)
    
    def update(self, base):
        self.pos = Vector(
                base.x + (PlayerTank.shieldSize * math.cos(math.radians(self.angle))),
                base.y + (PlayerTank.shieldSize * math.sin(math.radians(self.angle)))) 
        self.decreaseAlpha()

    def decreaseAlpha(self):
        self.alpha -= 0.02
        self.brightness -= 1
        if(self.alpha > 0.02):
            self.colour = simpleguiUtils.hsla(170, 100, self.brightness, self.alpha)

class PlayerTurret(Turret):

    def __init__(self, base, pos, playerTank):
        Turret.__init__(self, base, pos)
        self.playerTank = playerTank

    def shoot(self, clickedVel, type):
        targetVel = (clickedVel-self.getMuzzlePos()).normalize()
        if(not self.base.readyToFire) or (self.pos - clickedVel).length() < self.generator.length(): return
        if type == "shell":
            shot = Projectile(self.getMuzzlePos(), targetVel, self.projectileSpeed, "shell", (self.pos-clickedVel).length())
            self.base.recoil(shot)
        elif type == "homing":
            if self.playerTank.homingAmmo <= 0:
                return
            shot = HomingProjectile(self.getMuzzlePos(), targetVel)
            self.playerTank.homingAmmo -= 1
        self.base.readyToFire = False
        self.base.reloadCounter = 0
        return shot

    def update(self, mousePos):
        # Handles the rotation of vectors for the vertices of the tank
        self.updateRotation(Vector(mousePos[0], mousePos[1]))
        gen = self.generator.copy()
        self.mesh = list()
        for i in range(self.sides):
            self.mesh.append((self.pos + gen).getP())
            gen.rotate(360/self.sides)
