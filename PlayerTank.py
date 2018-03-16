from Line import *
from Tank import *


class PlayerTank(Tank):
    
    def __init__(self, pos):
        Tank.__init__(self, pos)
        self.mousePos = (0,0)
        self.cursor = simplegui.load_image('https://i.imgur.com/GYXjv5a.png')
        self.turret = PlayerTurret(self, pos)
        self.counter = 100
        self.isColliding = False
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
       # self.velocity.reflect(line.normal)
       # self.pos.add(self.velocity)
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

    def pickUpItem(self, items):
        pickUpRadius = 10
        for item in items:
            distance = item.getDistance(self.pos)
            if(distance < pickUpRadius + 3):
                # remove item from the map
                # apply item pickup
                self.applyHealthPack()
                items.remove(item)
                print("Applying health pack")
                print("removing item from map")
        return items

    def applyHealthPack(self):
        maxHealth = 100
        self.health += 25
        if self.health > maxHealth:
            self.health == maxHealth

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

    def draw(self, canvas):
        # draws a the line from the muzzle to the cursor position
        aimingLine = DottedLine(self.pos, Vector(self.mousePos[0], self.mousePos[1])).draw(canvas)
        canvas.draw_image(self.cursor, (self.cursor.get_width()/2, self.cursor.get_height()/2), 
                (self.cursor.get_width(), self.cursor.get_height()), self.mousePos, (20, 20))
        self.drawReloadStatus(canvas, self.mousePos, 9)
        Tank.draw(self, canvas)

    # Draws the circle surrounding the cursor point indicating how "reloaded" the tank is
    def drawReloadStatus(self, canvas, mousePos, radius):
        angle = (self.reloadCounter/self.interval) * 360
        for i in range(int(angle)):
            canvas.draw_point((mousePos[0]+(radius*math.cos(math.radians(i))),
                mousePos[1]+(radius*math.sin(math.radians(i)))), 'White')

class PlayerTurret(Turret):

    def __init__(self, base, pos):
        Turret.__init__(self, base, pos)

    def update(self, mousePos):
        # Handles the rotation of vectors for the vertices of the tank
        self.updateRotation(Vector(mousePos[0], mousePos[1]))
        gen = self.generator.copy()
        self.mesh = list()
        for i in range(self.sides):
            self.mesh.append((self.pos + gen).getP())
            gen.rotate(360/self.sides)