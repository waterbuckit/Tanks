import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector
from PlayerTank import PlayerTank
from EnemyTank import EnemyTank
from Explosion import Explosion

# Frame dimensions
WIDTH = 1200
HEIGHT = 800

class Interaction:

    def __init__(self, keyboard):
       self.player = PlayerTank(Vector(WIDTH/2, HEIGHT/2))
       self.keyboard = keyboard
       self.projectiles = []
       self.explosions = []
       self.enemyTank = EnemyTank(Vector(WIDTH/4, HEIGHT/4))
    
    def update(self):
        for explosion in self.explosions:
            explosion.update()
            if explosion.isFinished():
                self.explosions.remove(explosion)
        for projectile in self.projectiles:
            if not projectile.isWithinRange():
                self.explosions.append(Explosion(projectile.pos, projectile.getType()))
                self.projectiles.remove(projectile)
            if projectile.isColliding(self.enemyTank.getPosAndRadius()):
                self.enemyTank.decreaseHealth(projectile.getType())
                self.explosions.append(Explosion(projectile.pos, projectile.getType()))
                self.projectiles.remove(projectile)
        if simplegui.pygame.mouse.get_pressed()[2] == 1:
            shot = self.player.turret.shootMg(simplegui.pygame.mouse.get_pos())
            if shot is not None: self.projectiles.append(shot)
        if self.keyboard.space:
            if self.player.readyToFire:
                self.projectiles.append(self.player.turret.shootHomingMissile(simplegui.pygame.mouse.get_pos()))
        self.player.update(self.keyboard.forwards, self.keyboard.backwards, self.keyboard.left, self.keyboard.right, simplegui.pygame.mouse.get_pos())
        self.enemyTank.update(self.player)

    # Method for handling drawing all objects in the scene
    def drawHandler(self, canvas):
        self.update()
        self.player.draw(canvas)
        self.enemyTank.draw(canvas)
        for p in self.projectiles:
            p.draw(canvas)
        for explosion in self.explosions:
            explosion.draw(canvas)

    # Method for handling mouse clicks
    def mouseClickHandler(self, position):
        shot = self.player.turret.shoot(position)
        if shot is not None: self.projectiles.append(shot)
        shot2 = self.enemyTank.turret.shoot()
        if shot2 is not None: self.projectiles.append(shot2)
    # Method for handling key down
    def keyDownHandler(self, key):
        self.keyboard.keyDown(key)
    def keyUpHandler(self, key):
        self.keyboard.keyUp(key)

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

i = Interaction(Keyboard())
simplegui.pygame.mouse.set_visible(False)

# Frame initialisation
frame = simplegui.create_frame('Tanks', WIDTH, HEIGHT)
frame.set_mouseclick_handler(i.mouseClickHandler)
frame.set_draw_handler(i.drawHandler)
frame.set_keyup_handler(i.keyUpHandler)
frame.set_keydown_handler(i.keyDownHandler)
frame.start()
