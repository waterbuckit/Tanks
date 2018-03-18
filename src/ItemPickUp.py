from Tank import Tank
import random

class ItemPickUp():

    types = {"health":"Green", "shield":"Blue", "ammo":"Brown"}
    sizes = [3, 6, 9]

    def __init__(self, pos, game):
        self.type = random.choice(list(ItemPickUp.types.keys()))
        self.radius = random.choice(ItemPickUp.sizes)
        self.pos = pos
        self.game = game

    def pickupAction(self, player):
       if self.type == "health":
           self.applyHealth(player)
       elif self.type == "shield":
           self.applyShield(player)
       elif self.type == "ammo":
           pass
           #self.loadAmmo()

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
            player.shield += 10
            if player.shield > player.maxHealth:
                player.shield = player.maxHealth
        elif self.radius == ItemPickUp.sizes[1]:
            player.shield += 30
            if player.shield > player.maxHealth:
                player.shield = player.maxHealth
        elif self.radius == ItemPickUp.sizes[2]:
            player.shield += 50
            if player.shield > player.maxHealth:
                player.shield = player.maxHealth
        print(player.shield)

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

    def draw(self, canvas, color):
        canvas.draw_circle(self.pos.getP(), self.radius, self.radius, color, color)
