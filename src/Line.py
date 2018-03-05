from Vector import Vector

class Line:
    def __init__(self, point1, point2, dotted=False):
        self.pA = point1
        self.pB = point2
        self.length = (self.pA - self.pB).length()
        self.thickness = 3
        self.unit = (self.pB - self.pA).normalize()
        self.normal = self.unit.copy().rotateAnti()
        self.dotted = dotted

    def draw(self, canvas):
        canvas.draw_line(self.pA.getP(), self.pB.getP(), self.thickness, 'White')

class DottedLine:
    def __init__(self, point1, point2):
        self.pA = point1
        self.pB = point2
        self.vel = self.pB - self.pA
        self.length = self.vel.length()
        self.thickness = 3

    def draw(self, canvas):
        interval = 30
        newVel = self.vel.copy()/interval
        for i in range(0, interval):
            if i % 2 == 0:
                canvas.draw_line((self.pA+(newVel*i)).getP(), (self.pA+(newVel*(i+1))).getP(), self.thickness, '#303030')
