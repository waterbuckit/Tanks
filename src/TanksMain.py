#<<<<<<< HEAD
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector
from Tank import Tank
from PlayerTank import PlayerTank
from Explosion import Explosion
from Terrain import Terrain
import math
import Util
# Frame dimensions
WIDTH = 1200
HEIGHT = 800

class Interaction:
    def __init__(self, keyboard, terrain):
       self.terrain = terrain
       self.player = PlayerTank(Tank.newTankPos(terrain, WIDTH, HEIGHT), terrain.lines)
       self.keyboard = keyboard
       self.projectiles = []
       self.explosions = []
       self.enemies = []
       self.currentlyColliding = {}
       self.startEnemies = 0
       self.pauseCounter = 100
       self.isPaused = False
       for line in self.terrain.lines:
           self.currentlyColliding[(self.player, line)] = False

    def update(self):
        mousePos = self.getMousePos()
        for explosion in self.explosions:
            if explosion.isFinished() and explosion is not None:
                self.explosions.remove(explosion)
            explosion.update()
        for projectile in self.projectiles:
            if not projectile.isWithinRange() or self.hitWall(projectile):
                self.addExplosion(projectile.pos, projectile.getType(), projectile)
            else:
                if projectile.getType() == "homing":
                    projectile.update(simplegui.pygame.mouse.get_pos())
                else:
                    projectile.update()
            for enemy in self.enemies:
                if projectile.isColliding(enemy.getPosAndRadius()):
                    self.addExplosion(projectile.pos, projectile.getType(), projectile)
                    enemy.decreaseHealth(projectile.getType())
        for enemy in self.enemies:
                enemy.update(self.player)
                self.addProjectile(enemy, "shell", enemy.turret.aim(self.player))
        if simplegui.pygame.mouse.get_pressed()[2] == 1:
            self.addProjectile(self.player, "mg", Vector(mousePos[0], mousePos[1]))
        if self.keyboard.space:
            self.addProjectile(self.player, "homing", Vector(mousePos[0], mousePos[1]))
        
        for line in self.terrain.lines:
            if(self.player.isCollidingWithLine(line)):
                if(not self.currentlyColliding[(self.player, line)]):
                    self.player.collide(line)
                    self.currentlyColliding[(self.player, line)] = True
            elif(self.player.isCollidingWithLineTipA(line)):
                if(not self.currentlyColliding[(self.player, line)]):
                    self.player.collideTip(line.pA)
                    self.currentlyColliding[(self.player, line)] = True
            elif(self.player.isCollidingWithLineTipB(line)):
                if(not self.currentlyColliding[(self.player, line)]):
                    self.player.collideTip(line.pB)
                    self.currentlyColliding[(self.player, line)] = True
            else:
                self.currentlyColliding[(self.player, line)] = False
        self.player.update(self.keyboard.forwards, self.keyboard.backwards, self.keyboard.left, self.keyboard.right, simplegui.pygame.mouse.get_pos())
         
    def drawHandler(self, canvas):
        if self.keyboard.menu == True:
            self.drawMenu(canvas)
            return
        if(self.keyboard.p):
            self.isPaused = not self.isPaused
        if(not self.isPaused):
            self.update()
        self.terrain.drawWalls(canvas)
        for enemy in self.enemies:
            enemy.draw(canvas)
        for projectile in self.projectiles:
            projectile.draw(canvas)
        for explosion in self.explosions:
            explosion.draw(canvas)
        self.player.draw(canvas)
        if(self.isPaused):
            self.handlePause(canvas)

    def handlePause(self,canvas):
        self.pauseCounter += 0.1
        self.pauseCounter %= 100
        canvas.draw_circle((WIDTH/2,HEIGHT/2), Util.toRange(math.sin(self.pauseCounter),-1,1,0,100),1, "#accaf9", "#accaf9")
    
    def mouseClickHandler(self, position):
        self.addProjectile(self.player, "shell", Vector(position[0], position[1]))

    def keyDownHandler(self, key):
        self.keyboard.keyDown(key)

    def keyUpHandler(self, key):
        self.keyboard.keyUp(key)

    def getMousePos(self):
        return simplegui.pygame.mouse.get_pos()

    def addEnemy(self, enemy):
        self.enemies.append(enemy)

    def hitWall(self, projectile):
        for line in self.terrain.lines:
            if line.distanceTo(projectile.pos) <= projectile.rad + line.thickness and line.covers(projectile.pos):
                return True

    def addProjectile(self, origin, type, target):
        if type == "mg":
            shot = origin.turret.shootMg(target)
        else:
            shot = origin.turret.shoot(target, type)
        if shot is not None: self.projectiles.append(shot)

    def addExplosion(self, pos, type, source):
        if(source in self.projectiles):
            self.explosions.append(Explosion(pos, type))
            self.projectiles.remove(source)

    def drawMenu(self, canvas):
        canvas.draw_text("Tanks", (WIDTH / 2 - 70, HEIGHT / 2-50), 60, "White")
        canvas.draw_text("Press space to continue to the game", (WIDTH / 2 - 200, HEIGHT / 2 + 100), 30, "White")
        canvas.draw_text("Press 'C' to view controls", (WIDTH/2-140, HEIGHT/2+ 200), 30, "White")
        if self.keyboard.showControls == True:
            canvas.draw_text("WASD: Moves the player's tank", (100, 100), 20, "White")
            canvas.draw_text("Left click: Fire rocket", (100, 150), 20, "White")
            canvas.draw_text("Right click: Fire machine gun", (100, 200), 20, "White")
            canvas.draw_text("Space bar: Fire a homing missile", (100, 250), 20, "White")

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
        elif(key == simplegui.KEY_MAP['p']):
            self.p = True

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
            self.p = False
        elif(key == simplegui.KEY_MAP['c']):
            self.showControls = not self.showControls

simplegui.pygame.mouse.set_visible(False)
terrain = Terrain(WIDTH, HEIGHT)
terrain.genMaze(WIDTH, HEIGHT, 0, 0)

i = Interaction(Keyboard(), terrain)
for t in range(10):
     i.addEnemy(Tank(Tank.newTankPos(terrain, WIDTH, HEIGHT),i.terrain.lines))

i.startEnemies = len(i.enemies)
# Frame initialisation
frame = simplegui.create_frame('Tanks', WIDTH, HEIGHT)
frame.set_mouseclick_handler(i.mouseClickHandler)
frame.set_draw_handler(i.drawHandler)
frame.set_keyup_handler(i.keyUpHandler)
frame.set_keydown_handler(i.keyDownHandler)
frame.start()
