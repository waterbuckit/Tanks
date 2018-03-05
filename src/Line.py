from Vector import Vector

class Line:
    def __init__(self, point1, point2, color='White'):
        self.pA = point1
        self.pB = point2
        self.length = (self.pA - self.pB).length()
        self.thickness = 3
        self.unit = (self.pB - self.pA).normalize()
        self.normal = self.unit.copy().rotateAnti()
        self.color = color

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
