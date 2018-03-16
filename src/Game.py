from Tank import Tank
from PlayerTank import PlayerTank
from Terrain import Terrain

class Game:

    def __init__(self, width, height):
        self.canvasWidth = width
        self.canvasHeight = height
        self.score = 0
        self.lastRoundCount = 0
        self.currentRound = None
        self.enemies = []
        self.terrain = Terrain(self.canvasWidth, self.canvasHeight)
        self.player = PlayerTank(Tank.newTankPos(self.terrain, self.canvasWidth, self.canvasHeight), self.terrain.lines)

    def newRound(self, enemyCount):
       self.terrain.lines.clear()
       self.terrain.lines = self.terrain.genMaze(0, 0)
       for i in range(enemyCount):
           self.enemies.append(Tank(Tank.newTankPos(self.terrain, self.canvasWidth,
                                          self.canvasHeight), self.terrain.lines))
       self.lastRoundCount = enemyCount
