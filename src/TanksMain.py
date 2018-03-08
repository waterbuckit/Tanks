import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Frame dimensions
WIDTH = 1200
HEIGHT = 750

class Interaction:

    def __init__(self):
        pass

    # Method for handling drawing all objects in the scene
    def drawHandler(self, canvas):
        pass
    # Method for handling mouse clicks
    def mouseClickHandler(self, position):
        pass

i = Interaction()

# Frame initialisation
frame = simplegui.create_frame('Tanks', WIDTH, HEIGHT)
frame.set_mouseclick_handler(i.mouseClickHandler)
frame.set_draw_handler(i.drawHandler)
frame.start()
