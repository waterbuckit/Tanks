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
        self.gameOverStatus = False
        self.roundLives = 0

    def newRound(self, enemyCount):
        self.enemies.clear()
        self.terrain = Terrain(self.canvasWidth, self.canvasHeight, self)
        self.terrain.genMaze(0,0)
        for i in range(enemyCount):
            self.enemies.append(Tank(Tank.newTankPos(self.terrain, self.canvasWidth,
                                           self.canvasHeight), self))
        self.player = self.newPlayer()
        self.playerClonePos = self.player.pos.copy()
        self.roundCount = enemyCount
        self.score += self.roundCount

    def playerDeath(self):
        if self.roundLives <= 0:
            self.gameOver()
            return
        for enemy in self.enemies: enemy.health = 100
        self.player.pos = self.playerClonePos.copy()
        self.player.health = 100
        self.player.shieldStatus = 100
        self.player.trackMarks.clear()
        self.roundLives -= 1

    def gameOver(self):
        self.gameOverStatus = True

    def newPlayer(self):
        player = PlayerTank(Tank.newTankPos(self.terrain, self.canvasWidth, self.canvasHeight), self)
        return player

    def drawInfo(self, canvas):
        canvas.draw_text("ROUND: " + str(self.roundCount), (10, 20), 20, "White")
        canvas.draw_text("LIVES: " + str(self.roundLives), (10, 40), 20, "White")
        canvas.draw_text("MISSILES: " + str(self.player.homingAmmo), (10, 60), 20, "White")
        canvas.draw_text("Score: " + str(self.score), (10, 80), 20, "White")
