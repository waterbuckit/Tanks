from Tank import Tank
import Util
import random
import math
import SimpleGUICS2Pygame.codeskulptor_lib as simplegui

class ItemPickUp():

    types = {"health":"Green", "shieldStatus":"Blue", "missile":"Grey"}
    sizes = [3, 6, 9]

    def __init__(self, pos, game):
        self.type = random.choice(list(ItemPickUp.types.keys()))
        self.radius = random.choice(ItemPickUp.sizes)
        self.pos = pos
        self.game = game
        self.lineThickness = 2
        self.counter = 10

    def pickupAction(self, player):
       if self.type == "health":
           self.applyHealth(player)
       elif self.type == "shieldStatus":
           self.applyShield(player)
       elif self.type == "ammo":
           #self.loadAmmo()
           pass
       elif self.type == "missile":
            self.loadHoming(player)

    def applyHealth(self, player):
        if self.radius == ItemPickUp.sizes[0]:
            player.health += 10
            if player.health > player.maxHealth:
                player.health = player.maxHealth
        elif self.radius == ItemPickUp.sizes[1]:
            player.health += 30
            if player.health > player.maxHealth:
                player.health = player.maxHealth
        elif self.radius == ItemPickUp.sizes[2]:
            player.health += 50
            if player.health > player.maxHealth:
                player.health = player.maxHealth
        print(player.health)

    def applyShield(self, player):
        if self.radius == ItemPickUp.sizes[0]:
            player.shieldStatus += 10
            if player.shieldStatus > player.maxHealth:
                player.shieldStatus = player.maxHealth
        elif self.radius == ItemPickUp.sizes[1]:
            player.shieldStatus += 30
            if player.shieldStatus > player.maxHealth:
                player.shieldStatus = player.maxHealth
        elif self.radius == ItemPickUp.sizes[2]:
            player.shieldStatus += 50
            if player.shieldStatus > player.maxHealth:
                player.shieldStatus = player.maxHealth
        print(player.shieldStatus)

    def loadHoming(self, player):
        player.homingCount += self.radius//3

    def loadAmmo(self, type):
        if type == 'AP':
            self.damage = 50
            self.ammo= 5
        elif type == 'AtomBomb':
            self.damage = 500
            self.ammo = 1
        else:
            self.damage = 10
            self.ammo = -1
    
    def update(self):
        self.counter += 0.1
        self.counter %= 100
        self.lineThickness = int(Util.toRange(math.sin(self.counter), -1, 1, 1, 3))
        self.lineColor = simplegui.hsla(0, 100,100, 
                Util.toRange(math.sin(self.counter), -1, 1, 0.0, 1.0))

    def draw(self, canvas, color):
        canvas.draw_circle(self.pos.getP(), self.radius, self.lineThickness, self.lineColor, color)
