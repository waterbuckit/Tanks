from Vector import Vector
import random
import SimpleGUICS2Pygame.codeskulptor_lib as simplegui

class Explosion:
    def __init__(self, pos, projType):
        self.projType = projType
        self.pos = pos
        self.particles = []
        self.populateParticles()

    # generate the list of particles
    def populateParticles(self): 
        if(self.projType == "shell"):
            for i in range(random.randint(70,90)):
                self.particles.append(Particle(self.pos.copy(), 24, Vector(random.uniform(-10,10), random.uniform(-10, 10))))
        elif(self.projType == "homing"):
            for i in range(random.randint(70,90)):
                self.particles.append(Particle(self.pos.copy(), 231, Vector(random.uniform(-20,20), random.uniform(-20, 20)))) 
        elif(self.projType == "tankKill"):
            for i in range(random.randint(150,200)):
                self.particles.append(Particle(self.pos.copy(), 104, Vector(random.uniform(-30,30), random.uniform(-30,30))))
        else:
            for i in range(random.randint(30,50)):
                self.particles.append(Particle(self.pos.copy(), 66, Vector(random.uniform(-3,3), random.uniform(-3, 3))))
                        
    def isFinished(self):
        for particle in self.particles:
            if(not particle.alpha <= 0):
                return
        return True

    def update(self):
        for particle in self.particles:
            particle.update()

    def draw(self, canvas):
        for particle in range(len(self.particles)):
            #print("DRAWN particle no.: " + str(particle)+ " at " + str(self.particles[particle].pos.getP()))
            self.particles[particle].draw(canvas)

class Particle:
    def __init__(self, pos, hue, vel):
        self.pos = pos
        self.velocity = vel
        self.colour = '#FFFFFF'
        self.hue = hue
        self.saturation = 100.0
        self.brightness = 100.0
        self.alpha = 1.0
    
    def update(self):
        self.pos.add(self.velocity)
        self.velocity.multiply(0.85)
        self.decreaseAlpha()
   
    def decreaseAlpha(self):
        self.brightness -= 10
        self.alpha -= 0.1
        if(not self.alpha <= 0):
            self.colour = simplegui.hsla(self.hue, self.saturation, self.brightness, self.alpha)

    def draw(self, canvas):
        canvas.draw_circle(self.pos.getP(),2,1,self.colour,self.colour)
