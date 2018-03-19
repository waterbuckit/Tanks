import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector

class Menu:
    def __init__(self):
        pass

    def drawMenu(self, canvas, showControls, WIDTH, HEIGHT, highscore):
        canvas.draw_text("Tanks", (WIDTH / 2 - 70, HEIGHT / 2 - 50), 60, "White")
        canvas.draw_polygon([(900, 500), (900, 550), (1050, 550), (1050, 500)], 20, "Green", "Green")
        canvas.draw_text("Start", (945, 535), 30, "Black")
        canvas.draw_polygon([(525, 500), (525, 550), (675, 550), (675, 500)], 20, "Yellow", "Yellow")
        canvas.draw_text("Controls", (550, 535), 30, "Black")
        canvas.draw_polygon([(150, 500), (150, 550), (300, 550), (300, 500)], 20, "Red", "Red")
        canvas.draw_text("HighScore", (160, 540), 30, "Black")
        if (highscore == True):
            canvas.draw_polygon([(0, 0), (0, 460), (WIDTH-800, 460), (WIDTH-800, 0)], 20, "Black", "White")
            canvas.draw_text("HighScore", (160, 50), 20, "Black")
            with open("HighScores.txt", 'r') as f:
                highscores = f.readlines()
            highscores = [x.strip() for x in highscores]
            highscores = [int(x) for x in highscores]
            highscores.sort(reverse=True)
            top10 = highscores[:10]
            top10 = [str(x) for x in top10]
            y = 30
            z = 1
            for x in range(0,10):
                canvas.draw_text(str(z) + " :  "+ top10[x], (180, 50 + y), 20, "Black")
                z += 1
                y += 30


        if showControls == True:
            canvas.draw_polygon([(0, 0), (0, 460), (WIDTH, 460), (WIDTH, 0)], 20, "Black", "White")
            canvas.draw_text("WASD: Moves the player's tank", (100, 50), 20, "Black")
            canvas.draw_text("Left click: Fire rocket", (100, 100), 20, "Black")
            canvas.draw_text("Right click: Fire machine gun", (100, 150), 20, "Black")
            canvas.draw_text("Space bar: Fire a homing missile", (100, 200), 20, "Black")
            canvas.draw_text("Pickups can be found amongst the map, with color and size corresponding to type and effectiveness:", (100, 250), 20, "Black")
            canvas.draw_text("Health: A gift from the holy Panzer, increases tank health", (100, 300), 20, "Green")
            canvas.draw_text("Shield: More repelling than the friend-zone, increases tanks shield", (100, 350), 20, "Blue")
            canvas.draw_text("Missles: Paraphrasing Hawking, \"More bullets equals less bad guys\" adds homing missles to arsenal", (100, 400), 20, "Grey")


    def updateHighScore(self, score):
        with open("HighScores.txt", 'r') as f:
            highscores = f.readlines()
        highscores = [x.strip() for x in highscores]
        highscores = [int(x) for x in highscores]
        highscores.append(score)

        with open("HighScores.txt", 'w') as f:
            for i in highscores:
                f.write("%s\n" % i)


