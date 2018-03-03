from Vector import Vector
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class PlayerTank:
    
    def __init__(self, pos):
        self.rotation = 0
        self.width = 20
        self.height = 40 
        #self.turret = PlayerTurret(pos)
        self.pos = pos
        self.health = 100.0
        self.velocity = Vector(0,0)
        self.generator = Vector(0, -self.height/2)
        #self.mesh = Mesh(self.width, self.height, self.pos)
        
    def shoot(self, clickedPos):
        pass

    def terminalVelocity(self):
        return (self.velocity.length == 5)

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
        self.velocity.multiply(0.85)
        # For representing the front of the tank
        gen = self.generator.copy()
        self.frontPoint = Vector(self.pos.x, self.pos.y) + gen
        # For representing the back of the tank
        gen.rotate(180)
        self.backPoint = Vector(self.pos.x, self.pos.y) + gen
        #self.mesh.update()

    def draw(self, canvas):
        #self.mesh.draw(canvas)
        # Temporarily use a line to represent the current rotation
        canvas.draw_line((self.frontPoint.x, self.frontPoint.y), (self.backPoint.x, self.backPoint.y), 12, 'Red')

class PlayerTurret:
    
    def __init__(self, pos):
        self.width = 10
        self.height = 10
        self.pos = pos
        self.rotation = 0
        # self.mesh = Mesh(self.width, self.height, self.pos)
    
    def draw(self, canvas):
        pass
