import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector
from PlayerTank import PlayerTank
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
    
    def update(self):
        for explosion in self.explosions:
            explosion.update()
        pressed = simplegui.pygame.mouse.get_pressed()
        if pressed[2] == 1:
            shot = self.player.shootMg(simplegui.pygame.mouse.get_pos())
            self.projectiles.append(shot)
        self.player.update(self.keyboard.forwards, self.keyboard.backwards, self.keyboard.left, self.keyboard.right, simplegui.pygame.mouse.get_pos())

    # Method for handling drawing all objects in the scene
    def drawHandler(self, canvas):
        self.update()
        if self.keyboard.continueGame == False:
            canvas.draw_text("Tanks", (WIDTH / 2 - 70, HEIGHT / 2), 60, "White")
            canvas.draw_text("Press space to continue to the game", (WIDTH / 2 - 200, HEIGHT / 2 + 100), 30, "White")

        else:

            #draws a scoreboard
            canvas.draw_text("Level: ",(10, 15), 20, 'White')
            canvas.draw_text("Health: ",(10,35), 20, 'White')
            self.player.draw(canvas)
            for p in self.projectiles:
                if p is not None:
                    if p.isWithinRange():
                          p.draw(canvas)
                    else:
                        self.explosions.append(Explosion(p.pos, p.getType()))
                        print("Appended explosion")
                        self.projectiles.remove(p)
            for explosion in self.explosions:
                if explosion is not None:
                    if(explosion.isFinished()):
                        print("removed")
                        self.explosions.remove(explosion)
                        continue
                    explosion.draw(canvas)



    # Method for handling mouse clicks
    def mouseClickHandler(self, position):
        shot = self.player.shoot(position)
        self.projectiles.append(shot)
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
        #responsible for determining whether the title screen should be removed
        self.continueGame = False

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
            self.continueGame = True
    
    def keyUp(self, key):
        if(key == simplegui.KEY_MAP['w']):
            self.forwards = False
        elif(key == simplegui.KEY_MAP['s']):
            self.backwards = False
        elif(key == simplegui.KEY_MAP['a']):
            self.left = False
        elif(key == simplegui.KEY_MAP['d']):
            self.right = False


i = Interaction(Keyboard())
simplegui.pygame.mouse.set_visible(False)

# Frame initialisation
frame = simplegui.create_frame('Tanks', WIDTH, HEIGHT)
frame.set_mouseclick_handler(i.mouseClickHandler)
frame.set_draw_handler(i.drawHandler)
frame.set_keyup_handler(i.keyUpHandler)
frame.set_keydown_handler(i.keyDownHandler)
frame.start()
