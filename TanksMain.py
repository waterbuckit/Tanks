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

    # Method for handling drawing all objects in the scene
    def drawHandler(self, canvas):
        self.player.update(self.keyboard.forwards, self.keyboard.backwards, self.keyboard.left, self.keyboard.right)
        self.player.draw(canvas)
    # Method for handling mouse clicks
    def mouseClickHandler(self, position):
        pass
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
