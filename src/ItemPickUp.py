# Item Pickup
import PlayerTank

class ApplyItemPickUp(PlayerTank):

    def __init__(self):
        self.maxHealth = 100.0
        self.damage = 0
        self.ammoAP = 0
        self.ammoAtom = 0
        self.ammoReg = -1

    def applyHealthPack(self, type):
        if type == 's':
            self.health += 10
            if self.health> self.maxHealth:
                self.health == self.maxHealth
        elif type == 'm':
            self.health += 30
            if self.health > self.maxHealth:
                self.health == self.maxHealth
        elif type == 'l':
            self.health += 50
            if self.health > self.maxHealth:
                self.health == self.maxHealth
        return self.health


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

        return self.damage, self.ammo


    def applyShield(self):
        shieldHP = 50
        # duration the shield lasts for.
        duration = 30
        totalHP = self.health + shieldHP
        return totalHP, duration








