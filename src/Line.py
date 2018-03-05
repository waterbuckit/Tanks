from Vector import Vector
import SimpleGUICS2Pygame.codeskulptor_lib as simplegui

class Line:
    def __init__(self, point1, point2, color='White'):
        self.pA = point1
        self.pB = point2
        self.length = (self.pA - self.pB).length()
        self.thickness = 3
        self.unit = (self.pB - self.pA).normalize()
        self.normal = self.unit.copy().rotateAnti()
        self.hue = 0.0
        self.saturation = 0.0
        self.brightness = 100
        self.alpha = 1.0
        self.color = color
    def increaseAlpha(self):
        self.alpha -= 0.02
        if(not self.alpha <= 0):
            self.color = simplegui.hsla(self.hue, self.saturation, self.brightness, self.alpha)

    def draw(self, canvas):
        canvas.draw_line(self.pA.getP(), self.pB.getP(), self.thickness, self.color)

class DottedLine:
    def __init__(self, point1, point2, interval=100):
        self.pA = point1
        self.pB = point2
        self.vel = self.pB - self.pA
        self.length = self.vel.length()
        self.interval = interval
        self.thickness = 2

    def draw(self, canvas):
        newVel = self.vel.copy()/self.interval
        color = '#202020'
        for i in range(self.interval):
            if (i % 5 == 0):
                canvas.draw_line((self.pA+(newVel*i)).getP(), (self.pA+(newVel*(i+1))).getP(), self.thickness, color)
             
