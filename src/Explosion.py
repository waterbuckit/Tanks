from Vector import Vector
import random
import SimpleGUICS2Pygame.codeskulptor_lib as simplegui

class Explosion:
    def __init__(self, pos):
        self.pos = pos
        self.particles = []
        self.populateParticles()

    # generate the list of particles
    def populateParticles(self):
        for i in range(random.randint(30,50)):
            self.particles.append(Particle(self.pos, Vector(random.uniform(-3,3), random.uniform(-3, 3))))
        print(len(self.particles))

    def isFinished(self):
        for particle in self.particles:
            if(not particle.alpha <= 0):
                return
        return True
    def update(self):
        for particle in self.particles:
            particle.update()

    def draw(self, canvas):
        for particle in self.particles:
            particle.draw(canvas)

class Particle:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.colour = '#FFFFFF'
        self.hue = 0.0
        self.saturation = 0.0
        self.brightness = 100.0
        self.alpha = 1.0
    
    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.3)
        self.decreaseAlpha()
   
    def decreaseAlpha(self):
        self.alpha -= 0.3
        if(not self.alpha <= 0):
            self.colour = simplegui.hsla(self.hue, self.saturation, self.brightness, self.alpha)

    
    def draw(self, canvas):
        print("Drawn!")
        canvas.draw_circle(self.pos.getP(),3,1,self.colour,self.colour)
