import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector
from Tank import Tank
from PlayerTank import PlayerTank
from Explosion import Explosion
from Terrain import Terrain

# Frame dimensions
WIDTH = 1200
HEIGHT = 800

class Interaction:
    def __init__(self, keyboard, terrain):
       self.player = PlayerTank(Vector((WIDTH/2), (HEIGHT/2)))
       self.keyboard = keyboard
       self.projectiles = []
       self.explosions = []
       self.enemies = []
       self.terrain = terrain
       self.currentlyColliding = {}
       self.numberOfItems = 1
       for line in self.terrain.lines:
           self.currentlyColliding[(self.player, line)] = False

    def update(self):
        for explosion in self.explosions:
            if explosion.isFinished() and explosion is not None:
                self.explosions.remove(explosion)
            explosion.update()

        for projectile in self.projectiles:
            if not projectile.isWithinRange() or self.hitWall(projectile):
                self.addExplosion(projectile.pos, projectile.getType(), projectile)
                continue
            for enemy in self.enemies:
                if projectile.isColliding(enemy.getPosAndRadius()):
                    self.addExplosion(projectile.pos, projectile.getType(), projectile)
                    enemy.decreaseHealth(projectile.getType())
        for enemy in self.enemies:
                enemy.update(self.player)
                self.addProjectile(enemy, "shell", enemy.turret.aimPos.getP())
        if simplegui.pygame.mouse.get_pressed()[2] == 1:
            self.addProjectile(self.player, "mg", simplegui.pygame.mouse.get_pos())
        if self.keyboard.space:
            self.addProjectile(self.player, "homing", simplegui.pygame.mouse.get_pos())
        
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
        self.update()
        self.terrain.drawWalls(canvas)
        self.terrain.drawItemPickUp(canvas, self.player)
        for enemy in self.enemies:
            enemy.draw(canvas)
        for projectile in self.projectiles:
            projectile.draw(canvas)
        for explosion in self.explosions:
            explosion.draw(canvas)
        self.player.draw(canvas)

    def mouseClickHandler(self, position):
        self.addProjectile(self.player, "shell", position)

    def keyDownHandler(self, key):
        self.keyboard.keyDown(key)

    def keyUpHandler(self, key):
        self.keyboard.keyUp(key)

    def addEnemy(self, enemy):
        self.enemies.append(enemy)

    def hitWall(self, projectile):
        for line in self.terrain.lines:
            if line.distanceTo(projectile.pos) <= projectile.rad + line.thickness and line.covers(projectile.pos):
                return True

    def addProjectile(self, origin, type, target):
        target = Vector(target[0], target[1])
        if type == "mg":
            shot = origin.turret.shootMg(target)
        else:
            shot = origin.turret.shoot(target, type)
        if shot is not None: self.projectiles.append(shot)

    def addExplosion(self, pos, type, source):
        self.explosions.append(Explosion(pos, type))
        self.projectiles.remove(source)

class Keyboard:
    def __init__(self):
        self.forwards = False
        self.backwards = False
        self.left = False
        self.right = False
        self.space = False

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


simplegui.pygame.mouse.set_visible(False)
terrain = Terrain(WIDTH, HEIGHT)
terrain.genMaze(WIDTH, HEIGHT, 0, 0)

i = Interaction(Keyboard(), terrain)
for t in range(5):
     i.addEnemy(Tank.newEnemy(terrain, WIDTH, HEIGHT))

# Frame initialisation
frame = simplegui.create_frame('Tanks', WIDTH, HEIGHT)
frame.set_mouseclick_handler(i.mouseClickHandler)
frame.set_draw_handler(i.drawHandler)
frame.set_keyup_handler(i.keyUpHandler)
frame.set_keydown_handler(i.keyDownHandler)
frame.start()