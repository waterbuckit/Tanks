from Tank import Tank
import random

class ItemPickUp():

    types = {"health":"Green", "shieldStatus":"Blue", "ammo":"Brown"}
    sizes = [3, 6, 9]

    def __init__(self, pos, game):
        self.type = random.choice(list(ItemPickUp.types.keys()))
        self.radius = random.choice(ItemPickUp.sizes)
        self.pos = pos
        self.game = game

    def pickupAction(self, player):
       if self.type == "health":
           self.applyHealth(player)
       elif self.type == "shieldStatus":
           self.applyShield(player)
       elif self.type == "ammo":
           self.loadAmmo(player)

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

    def loadAmmo(self, player):
        if self.radius == ItemPickUp.sizes[0]:
            player.homingAmmo += 1
        elif self.radius == ItemPickUp.sizes[1]:
            player.homingAmmo += 2
        elif self.radius == ItemPickUp.sizes[2]:
            player.homingAmmo += 3
        print(player.homingAmmo)

    def draw(self, canvas, color):
        canvas.draw_circle(self.pos.getP(), self.radius, self.radius, color, color)
