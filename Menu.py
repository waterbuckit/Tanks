import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
class Menu:
    def __init__(self):
        pass

    def drawMenu(self, canvas, showControls, WIDTH, HEIGHT):
        canvas.draw_text("Tanks", (WIDTH / 2 - 70, HEIGHT / 2-50), 60, "White")
        canvas.draw_text("Press space to continue to the game", (WIDTH / 2 - 200, HEIGHT / 2 + 100), 30, "White")
        canvas.draw_text("Press 'C' to view controls", (WIDTH/2-140, HEIGHT/2+ 200), 30, "White")
        if showControls == True:
            canvas.draw_text("WASD: Moves the player's tank", (100, 100), 20, "White")
            canvas.draw_text("Left click: Fire rocket", (100, 150), 20, "White")
            canvas.draw_text("Right click: Fire machine gun", (100, 200), 20, "White")
            canvas.draw_text("Space bar: Fire a homing missile", (100, 250), 20, "White")
