import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import SimpleGUICS2Pygame.codeskulptor_lib as simpleguitools
import math
from Vector import Vector
import copy
class Projectile:
    def __init__(self, pos, vel, speed, projType, rng=500, isTrailed=True, rad=3, color='White'):
        self.projType = projType
        self.pos = pos
        self.vel = vel * speed
        self.rad = rad
        self.range = rng
        self.travelled = 0
        self.isTrailed = isTrailed
        self.trail = Trail(pos, rad)
        self.color = color

    def isColliding(self, other):
        otherPos = other[0]
        otherRad = other[1]
        return self.pos.x > otherPos[0] - otherRad and self.pos.x < otherPos[0] + otherRad and self.pos.y > otherPos[1] - otherRad and self.pos.y < otherPos[1] + otherRad
    
    def getVel(self):
        return self.vel.getP()
    
    def isWithinRange(self):
        return self.travelled + self.vel.length() < self.range

    def update(self):
        self.travelled += self.vel.length()
        self.rad -= self.rad / (self.range / self.vel.length())
        self.pos += self.vel
        self.trail.update(self.pos, self.rad)
    
    def draw(self, canvas):
        self.update()
        canvas.draw_circle(self.pos.getP(), self.rad, 1, self.color, self.color)
        if self.isTrailed:
            self.trail.draw(canvas)
    
    def getType(self):
        return self.projType

# Projectile for following mouse cursor
class HomingProjectile:
    def __init__(self, pos, vel,isTrailed=True,rng= 3000):
        self.acceleration = Vector(0,0)
        self.pos = pos
        self.vel = vel.normalize()
        self.rad = 3
        self.range = rng
        self.travelled = 0
        self.isTrailed = isTrailed
        self.trail = Trail(pos, self.rad)
        self.color = 'Green'
        self.projType = "homing"
        self.maxSpeed = 6
        self.maxForce = 0.1
   
    def applyForce(self, force): 
    # We could add mass here if we want A = F / M for extra deliciousness
        self.acceleration.add(force);
    
    def isAtMouseLocation(self):
        mousePos = simplegui.pygame.mouse.get_pos()
        mouse = Vector(mousePos[0], mousePos[1])
        return (self.pos.getDistance(mouse) < 3)

    def isColliding(self, other):
        otherPos = other[0]
        otherRad = other[1]
        return (self.pos.x > otherPos[0] - otherRad and self.pos.x < otherPos[0] + otherRad and self.pos.y > otherPos[1] - otherRad and self.pos.y < otherPos[1] + otherRad)
    
    # Steering = desired - velocity 
    def update(self, mousePos):
        mouse = Vector(mousePos[0], mousePos[1])
        # set the magnitude...
        desired = (mouse - self.pos).normalize().multiply(self.maxSpeed)
        steering = desired - self.vel
        steering.limit(self.maxForce)
        self.applyForce(steering)

        self.vel.add(self.acceleration)
        self.vel.limit(self.maxSpeed)
        
        self.pos.add(self.vel)
        self.trail.update(self.pos, self.rad)
        self.acceleration.multiply(0)

    def draw(self,canvas):
        mousePos = simplegui.pygame.mouse.get_pos()
        self.update(mousePos)
        canvas.draw_circle(self.pos.getP(), self.rad, 1, self.color, self.color)
        if self.isTrailed:
            self.trail.draw(canvas)
    
    def getType(self):
        return self.projType
 
    def getVel(self):
        return self.vel.getP()

    def isWithinRange(self):
        return self.travelled < self.range and not self.isAtMouseLocation()
    
    def isColliding(self, other):
        otherPos = other[0]
        otherRad = other[1]
        return self.pos.x > otherPos[0] - otherRad and self.pos.x < otherPos[0] + otherRad and self.pos.y > otherPos[1] - otherRad and self.pos.y < otherPos[1] + otherRad

class Trail:
    def __init__(self, pos, rad):
        self.trailCircles = []
        self.trailSmoke = []
        self.smokeCounter = 5
        self.populateTrail(pos,rad)
 
    def populateTrail(self,pos,rad):
        for i in range(10):
            self.trailCircles.append(TrailCircle(pos,rad))
 
    def update(self, pos, rad):
        # Ensure that the first element of the trail is at the position of the projectile
        firstElement = self.trailCircles[0].update(pos, rad)
        # Update this element with the position of the element i-1 in the array
        self.smokeCounter += 1
        self.smokeCounter %= 5
        if(self.smokeCounter % 5 == 0):
            self.trailSmoke.append(TrailSmoke(self.trailCircles[len(self.trailCircles)-1].getPos(),
                ((rad/(len(self.trailCircles)-1)*3))))
        for smoke in self.trailSmoke:
            if(smoke.alpha <= 0):
                self.trailSmoke.remove(smoke)
                continue
            smoke.update()
        for i in range(1,len(self.trailCircles)):
            self.trailCircles[i].update(self.trailCircles[i-1].getPos(), (rad/i)*3) 

    def draw(self, canvas):
        for i in self.trailCircles:
            i.draw(canvas)
        for smoke in self.trailSmoke:
            smoke.draw(canvas)

class TrailSmoke:
    def __init__(self, pos, rad):
        self.pos = pos.copy()
        self.rad = rad
        self.colour = 'White'
        self.hue = 0.0
        self.saturation = 0.0
        self.brightness = 100
        self.alpha = 1.0

    def update(self):
        self.rad += 0.5
        self.alpha -= 0.02
        if(not self.alpha <= 0):
            self.colour = simpleguitools.hsla(self.hue, self.saturation, self.brightness, self.alpha)

    def draw(self, canvas):
        canvas.draw_circle((self.pos.x, self.pos.y), self.rad, 1, self.colour, self.colour)

class TrailCircle:
    def __init__(self, pos, rad):
        self.pos = pos
        self.rad = rad
        
    def getPos(self):
        return self.pos
    
    def update(self, otherPos, rad):
        # set the new position at half the distance between this element and the other one
        self.rad = rad
        self.pos += (otherPos - self.pos).multiply(0.5)
    
    def draw(self, canvas):
        canvas.draw_circle((self.pos.x, self.pos.y), self.rad, 1, 'Red', 'Orange')
