#░▀█▀░█▀█░█▀█░█░█░█▀▀
#░░█░░█▀█░█░█░█▀▄░▀▀█
#░░▀░░▀░▀░▀░▀░▀░▀░▀▀▀

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector
from Game import Game
from Tank import Tank
from PlayerTank import PlayerTank
from Explosion import Explosion
from Terrain import Terrain
from Menu import Menu
from Projectile import *
import math
import Util
# Frame dimensions
WIDTH = 1200
HEIGHT = 800

class Interaction:
    
    menu = Menu()
    
    def __init__(self, keyboard, game):
       self.game = game
       self.game.newRound(1)
       self.keyboard = keyboard
       self.projectiles = []
       self.explosions = []
       self.trails = []
       self.currentlyColliding = {}
       self.pauseCounter = 100
       self.isPaused = False
       self.setMappings()
       self.mousePos = self.game.player.pos
       for line in self.game.terrain.lines:
           self.currentlyColliding[(self.game.player, line)] = False

    def update(self):
        self.mousePos = self.getMousePos() 
        if(len(self.game.enemies) == 0):
            self.handleGameWin()
        for explosion in self.explosions:
            explosion.update()
            if explosion.isFinished():
                self.explosions.remove(explosion)
                continue
        for enemy in self.game.enemies:
            enemy.update(self.game.player)
            self.addProjectile(enemy, "shell", enemy.turret.aim(self.game.player))
        for projectile in self.projectiles:
            projectile.update()
            if not projectile.isWithinRange() or self.hitWall(projectile):
                self.addExplosion(projectile)
                continue
            # colliding with shield
            if(projectile.isColliding((self.game.player.pos.getP(), self.game.player.shieldSize)) 
                    and self.game.player.shieldStatus > 0):
                self.addExplosion(projectile)
                self.game.player.shield.receiveHit(projectile.pos)
                #self.game.player.decreaseShield(projectile.getType())
                continue
            # colliding with the actual player
            if(projectile.isColliding((self.game.player.getPosAndRadius()))):
                self.addExplosion(projectile)
                self.game.player.decreaseHealth(projectile.getType())
                continue
            for enemy in self.game.enemies:
                if projectile.isColliding(enemy.getPosAndRadius()):
                    self.addExplosion(projectile)
                    enemy.decreaseHealth(projectile.getType())
                    if(enemy.health <= 0):
                        self.addProjlessExplosion(enemy.pos)
                        self.game.enemies.remove(enemy)
        for trail in self.trails:
            if(trail.isFinished()):
                self.trails.remove(trail)
            else:
                trail.update()
        self.checkRightClick()
        self.checkSpacebar()
        for line in self.game.terrain.lines:
            if(self.game.player.isCollidingWithLine(line) and 
                    not self.currentlyColliding[(self.game.player, line)]):
                self.game.player.collide(line)
                self.currentlyColliding[(self.game.player, line)] = True
            elif(self.game.player.isCollidingWithLineTipA(line) and 
                    not self.currentlyColliding[(self.game.player, line)]):
                self.game.player.collideTip(line.pA)
                self.currentlyColliding[(self.game.player, line)] = True
            elif(self.game.player.isCollidingWithLineTipB(line) and 
                    not self.currentlyColliding[(self.game.player, line)]):
                self.game.player.collideTip(line.pB)
                self.currentlyColliding[(self.game.player, line)] = True
            else:
                self.currentlyColliding[(self.game.player, line)] = False
        self.game.player.update(self.keyboard.forwards, self.keyboard.backwards, 
                self.keyboard.left, self.keyboard.right, self.mousePos.getP())
         
    def drawHandler(self, canvas):
        if self.keyboard.menu:
            self.menu.drawMenu(canvas, self.keyboard.showControls, WIDTH, HEIGHT)
            return
        if not self.keyboard.p:
            self.update()
        self.game.terrain.drawWalls(canvas)
        self.game.terrain.drawItemPickUp(canvas, self.game.player)
        self.game.drawInfo(canvas)
        for enemy in self.game.enemies:
            enemy.draw(canvas)
        for projectile in self.projectiles:
            projectile.draw(canvas)
        for explosion in self.explosions:
            explosion.draw(canvas)
        for trail in self.trails:
            trail.draw(canvas)
        self.game.player.draw(canvas)
        self.handlePause(canvas, self.keyboard.p)

    def handlePause(self,canvas, paused):
        if not paused: return
        self.pauseCounter += 0.1
        self.pauseCounter %= 100
        canvas.draw_circle((WIDTH/2,HEIGHT/2), 
                Util.toRange(math.sin(self.pauseCounter),-1,1,0,100),1,
                "#accaf9", "#accaf9")

    def handleGameWin(self): 
        # Clear all the lists
        self.game.newRound(game.roundCount+1)
        self.projectiles.clear()
        self.explosions.clear()
        #self.game.enemies.clear()
        self.trails.clear()
        self.currentlyColliding.clear()
        self.setMappings()

    def mouseClickHandler(self, position):
        self.addProjectile(self.game.player, "shell", Vector(position[0], position[1]))

    def checkRightClick(self):
        if simplegui.pygame.mouse.get_pressed()[2] == 1:
            self.addProjectile(self.game.player, "mg", self.mousePos)

    def checkSpacebar(self):
        if self.keyboard.space:
            self.addProjectile(self.game.player, "homing", self.mousePos)

    def keyDownHandler(self, key):
        self.keyboard.keyDown(key)

    def keyUpHandler(self, key):
        self.keyboard.keyUp(key)

    def getMousePos(self):
        mouseTup = simplegui.pygame.mouse.get_pos()
        return Vector(mouseTup[0], mouseTup[1])

    def hitWall(self, projectile):
        for line in self.game.terrain.lines:
            if(line.distanceTo(projectile.pos) <= projectile.rad + line.thickness
                    and line.covers(projectile.pos)):
                return True

    def addProjectile(self, origin, type, target):
        if type == "mg":
            shot = origin.turret.shootMg(target)
        else:
            shot = origin.turret.shoot(target, type)
        if shot is not None: 
            self.projectiles.append(shot)
            if(not shot.projType == "mg"):
                self.trails.append(SmokeTrail(shot, self.projectiles))
    
    def addProjlessExplosion(self, pos):
        self.explosions.append(Explosion(pos, "tankKill"))

    def addExplosion(self, source):
        if(source in self.projectiles):
            self.explosions.append(Explosion(source.pos, source.getType()))
            self.projectiles.remove(source)
    
    def setMappings(self):
       for line in self.game.terrain.lines:
           self.currentlyColliding[(self.game.player, line)] = False

class Keyboard:
    def __init__(self):
        self.forwards = False
        self.backwards = False
        self.left = False
        self.right = False
        self.space = False
        self.p = False
        self.menu = True
        self.showControls = False

    def keyDown(self, key):
        if(key == simplegui.KEY_MAP['w']):
            self.forwards = True
        elif(key == simplegui.KEY_MAP['s']):
            self.backwards = True
        elif(key == simplegui.KEY_MAP['a']):
            self.left = True
        elif(key == simplegui.KEY_MAP['d']):
            self.right = True
        elif(key == simplegui.KEY_MAP['space']):
            self.space = True

    def keyUp(self, key):
        if(key == simplegui.KEY_MAP['w']):
            self.forwards = False
        elif(key == simplegui.KEY_MAP['s']):
            self.backwards = False
        elif(key == simplegui.KEY_MAP['a']):
            self.left = False
        elif(key == simplegui.KEY_MAP['d']):
            self.right = False
        elif(key == simplegui.KEY_MAP['space']):
            self.space = False
            self.menu = False
        elif(key == simplegui.KEY_MAP['p']):
            self.p = not self.p
        elif(key == simplegui.KEY_MAP['c']):
            self.showControls = not self.showControls

game = Game(1200, 800)
i = Interaction(Keyboard(), game)
simplegui.pygame.mouse.set_visible(False)

# Frame initialisation
frame = simplegui.create_frame('Tanks', WIDTH, HEIGHT)
frame.set_mouseclick_handler(i.mouseClickHandler)
frame.set_draw_handler(i.drawHandler)
frame.set_keyup_handler(i.keyUpHandler)
frame.set_keydown_handler(i.keyDownHandler)
frame.start()
