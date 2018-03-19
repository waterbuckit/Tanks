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
        self.enemyPositions = []
        self.currentRound = None
        self.playerClonePos = None
        self.terrain = None
        self.player = None
        self.roundLives = 3

    def newRound(self, enemyCount):
       self.enemies.clear()
       self.terrain = Terrain(self.canvasWidth, self.canvasHeight, self)
       self.terrain.genMaze(0,0)
       for i in range(enemyCount):
           self.enemies.append(Tank(Tank.newTankPos(self.terrain, self.canvasWidth,
                                          self.canvasHeight), self))
       self.enemyPositions = list(self.enemies)
       self.player = self.newPlayer()
       self.playerClonePos = self.player.pos.copy()
       self.roundCount = enemyCount

    def playerDeath(self):
       if self.roundLives <= 0:
           self.gameOver()
       self.player.pos = self.playerClonePos.copy()
       self.enemies = list(self.enemyPositions)
       self.player.health = 100
       self.player.shield = 100
       self.player.trackMarks.clear()
       self.roundLives -= 1

    def newPlayer(self):
        player = PlayerTank(Tank.newTankPos(self.terrain, self.canvasWidth, self.canvasHeight), self)
        return player

    def drawInfo(self, canvas):
        canvas.draw_text("Round: " + str(self.roundCount), (10, 20), 20, "White")
        canvas.draw_text("Lives: " + str(self.roundLives), (10, 40), 20, "White")
