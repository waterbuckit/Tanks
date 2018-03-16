from Tank import Tank
from PlayerTank import PlayerTank
from Terrain import Terrain

class Game:

    def __init__(self, width, height):
        self.canvasWidth = width
        self.canvasHeight = height
        self.score = 0
        self.roundCount = 0
        self.enemies = []
        self.currentRound = None
        self.terrain = None
        self.player = None

    def newRound(self, enemyCount):
       self.terrain = Terrain(self.canvasWidth, self.canvasHeight)
       self.terrain.genMaze(0,0)
       for i in range(enemyCount):
           self.enemies.append(Tank(Tank.newTankPos(self.terrain, self.canvasWidth,
                                          self.canvasHeight), self))
       self.player = self.newPlayer()
       self.roundCount = enemyCount

    def newPlayer(self):
        return PlayerTank(Tank.newTankPos(self.terrain, self.canvasWidth, self.canvasHeight), self)

    def drawInfo(self, canvas):
        canvas.draw_text("Round: " + str(self.roundCount), (10, 20), 20, "White")
