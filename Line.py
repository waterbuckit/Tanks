from Vector import Vector

class Line:
    def __init__(self, point1, point2):
        self.pA = point1
        self.pB = point2
        self.thickness = 3
        self.unit = (self.pB - self.pA).normalize()
        self.normal = self.unit.copy().rotateAnti()
        
    def draw(self, canvas):
        canvas.draw_line(self.pA.getP(), self.pB.getP(), self.thickness, 'White')
