import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector
from PlayerTank import PlayerTank

# Frame dimensions
WIDTH = 1200
HEIGHT = 800

class Interaction:

    def __init__(self, keyboard):
       self.player = PlayerTank(Vector(WIDTH/2, HEIGHT/2))
       self.keyboard = keyboard
       self.projectiles = []
    # Method for handling drawing all objects in the scene
    def drawHandler(self, canvas):
        simplegui.pygame.mouse.set_visible(False)
        self.player.update(self.keyboard.forwards, self.keyboard.backwards, self.keyboard.left, self.keyboard.right, simplegui.pygame.mouse.get_pos())
        self.player.draw(canvas)
        for p in self.projectiles:
            if p is not None:
                if p.isWithinRange():
                    p.draw(canvas)
                else:
                    self.projectiles.remove(p)
    # Method for handling mouse clicks
    def mouseClickHandler(self, position):
        pressed = simplegui.pygame.mouse.get_pressed()
        print(str(pressed))
        shot = self.player.shoot(position)
        shotmg = self.player.shootMg(position)
        self.projectiles.append(shot)
        self.projectiles.append(shotmg)
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

    def keyDown(self, key):
        if(key == simplegui.KEY_MAP['w']):
            self.forwards = True
        elif(key == simplegui.KEY_MAP['s']):
            self.backwards = True
        elif(key == simplegui.KEY_MAP['a']):
            self.left = True
        elif(key == simplegui.KEY_MAP['d']):
            self.right = True
    
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

# Frame initialisation
frame = simplegui.create_frame('Tanks', WIDTH, HEIGHT)
frame.set_mouseclick_handler(i.mouseClickHandler)
frame.set_draw_handler(i.drawHandler)
frame.set_keyup_handler(i.keyUpHandler)
frame.set_keydown_handler(i.keyDownHandler)
frame.start()
