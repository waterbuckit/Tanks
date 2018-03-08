import math
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
        return self.travelled < self.range
    
    def update(self):
        hyp = self.vel.length()
        self.travelled += hyp
        self.rad -= self.rad / (self.range / hyp)
        self.pos += self.vel
        self.trail.update(self.pos, self.rad)
    
    def draw(self, canvas):
        self.update()
        canvas.draw_circle(self.pos.getP(), self.rad, 1, self.color, self.color)
        if self.isTrailed:
            self.trail.draw(canvas)
    
    def getType(self):
        return self.projType

class Trail:
    def __init__(self, pos, rad):
        self.trailCircles = []
        self.populateTrail(pos,rad)
 
    def populateTrail(self,pos,rad):
        for i in range(10):
            self.trailCircles.append(TrailCircle(pos,rad))
 
    def update(self, pos, rad):
        # Ensure that the first element of the trail is at the position of the projectile
        firstElement = self.trailCircles[0].update(pos, rad)
        # Update this element with the position of the element i-1 in the array
        for i in range(1,len(self.trailCircles)):
            self.trailCircles[i].update(self.trailCircles[i-1].getPos(), (rad/i)*3) 

    def draw(self, canvas):
        for i in self.trailCircles:
            i.draw(canvas)

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
