import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector

class Menu:
    def __init__(self):
        pass

    def drawMenu(self, canvas, showControls, WIDTH, HEIGHT, highscore):
        canvas.draw_text("Tanks", (WIDTH / 2 - 70, HEIGHT / 2 - 50), 60, "White")
        canvas.draw_polygon([(900, 500), (900, 550), (1100, 550), (1100, 500)], 20, "Green", "Green")
        canvas.draw_text("Press space to Start", (905, 535), 25, "Black")
        canvas.draw_polygon([(500, 500), (500, 550), (700, 550), (700, 500)], 20, "Yellow", "Yellow")
        canvas.draw_text("Press c for Controls", (505, 535), 25, "Black")
        canvas.draw_polygon([(100, 500), (100, 550), (300, 550), (300, 500)], 20, "Red", "Red")
        canvas.draw_text("press h for HighScore", (105, 535), 23, "Black")

        if (highscore == True):
            canvas.draw_polygon([(100, 0), (100, 430), (300, 430), (300, 0)], 20, "Black", "Grey")
            canvas.draw_text("Top 10 Scores", (160, 50), 20, "Black")
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
            canvas.draw_polygon([(0, 0), (0, 470), (WIDTH, 470), (WIDTH, 0)], 20, "Black", "White")
            canvas.draw_text("WASD: Moves the player's tank", (100, 50), 20, "Black")
            canvas.draw_text("Left click: Fire rocket", (100, 100), 20, "Black")
            canvas.draw_text("Right click: Fire machine gun", (100, 150), 20, "Black")
            canvas.draw_text("Space bar: Fire a homing missile", (100, 200), 20, "Black")
            canvas.draw_text("p: Pauses game", (100, 250), 20, "Black")
            canvas.draw_text("Pickups can be found amongst the map, with color and size corresponding to type and effectiveness:", (100, 300), 20, "Black")
            canvas.draw_text("Health: A gift from the holy Panzer, increases tank health", (100, 350), 20, "Green")
            canvas.draw_text("Shield: More repelling than the friend-zone, increases tanks shield", (100, 400), 20, "Blue")
            canvas.draw_text("Missles: Paraphrasing Hawking, \"More bullets equals less bad guys\" adds homing missles to arsenal", (100, 450), 20, "Grey")


    def updateHighScore(self, score):
        with open("HighScores.txt", 'r') as f:
            highscores = f.readlines()
        highscores = [x.strip() for x in highscores]
        highscores = [int(x) for x in highscores]
        highscores.append(score)

        with open("HighScores.txt", 'w') as f:
            for i in highscores:
                f.write("%s\n" % i)


