import pygame
import random
import webbrowser
pygame.init()

WINDOW_SIZE = (500, 500)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Simon Memory Game")
BUTTON_COLOR = "#80ffc8"
simonLogo = pygame.image.load("Assets/simonLogo.png")
simonLogo = pygame.transform.scale(simonLogo, (348, 67))
musicDict = {(0, 255, 0):"Sounds/green.wav",
             (255, 0, 0):"Sounds/red.wav",
             (255, 255, 0):"Sounds/yellow.wav",
             (0, 0, 255):"Sounds/blue.wav"}


class RectButton:
    def __init__(self, surface, color, x, y, width, height, index, colorsList):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = index
        self.colorsList = colorsList

        self.COLOR_CONST = self.colorsList[self.index]
        self.rect = None

    def displayRect(self):
        self.rect = pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))

    def get_color(self):
        return self.color

    def set_color(self, newColor):
        self.color = newColor


def sleep(ms):
    while ms > 0:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        ms -= 10



def rules():
    rulesBG = pygame.image.load("Assets/rulesBG.png")
    rulesBG = pygame.transform.scale(rulesBG, WINDOW_SIZE)
    font = pygame.font.SysFont("Arial", 60, "bold")
    font2 = pygame.font.SysFont("Arial", 20)
    font3 = pygame.font.SysFont("Arial", 30)
    while True:
        window.fill((0, 0, 0))
        window.blit(rulesBG, (0, 0))

        window.blit(font.render("Rules", True, (0, 0, 0)), (160, 20))

        y = 100
        with open("rules.txt", "r") as f:
            for line in f.readlines():
                window.blit(font2.render(line[:-1], True, (0, 0, 0)), (20, y))
                y += 20
        url = "https://en.wikipedia.org/wiki/Simon_(game)"
        url_label = window.blit(font2.render(url, True,
                                 (0, 0, 255)), (165, (y-20)))

        pygame.draw.rect(window, (0, 0, 255), (10, 10, 40, 40))
        xButton = window.blit(font3.render("X", True, (255, 255, 255)), (20, 12))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if url_label.collidepoint(event.pos):
                    webbrowser.open(url)

                if xButton.collidepoint(event.pos):
                    menu()

        pygame.display.update()


def menu():
    font1 = pygame.font.SysFont("Arial", 20)
    font2 = pygame.font.SysFont("Arial", 40, "bold")
    while True:
        window.fill((0, 0, 0))

        window.blit(simonLogo, (70, 20))

        window.blit(font1.render("An enjoyable memory game, suitable for all ages", True, (255, 255, 255)),
                    (70, 100))

        playButton = pygame.draw.rect(window, BUTTON_COLOR, (140, 200, 200, 80))
        window.blit(font2.render("PLAY", True, (255, 255, 255)), (190, 220))

        rulesButton = pygame.draw.rect(window, BUTTON_COLOR, (140, 320, 200, 80))
        window.blit(font2.render("Rules", True, (255, 255, 255)), (185, 340))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.collidepoint(event.pos):
                    main()

                if rulesButton.collidepoint(event.pos):
                    rules()

        pygame.display.update()


def drawButtons(buttons):
    for button in buttons:
        button.displayRect()


def createButtons(colorsList):
    x = 90
    y = 120
    buttons = []
    for index, color in enumerate(colorsList):
        rect = RectButton(window, color, x, y, 150, 150, index, colorsList)
        buttons.append(rect)

        if x == 90 and y == 120:
            x += 170
        elif x == 260 and y == 120:
            x = 90
            y += 170
        elif x == 90 and y == 290:
            x += 170
    return buttons


def buttonPressed(colorsList, colorsList2, b, buttons, neonColorsList):
    index = colorsList.index(b.COLOR_CONST)
    b.set_color(neonColorsList[index])
    sound = pygame.mixer.Sound(musicDict[b.COLOR_CONST])
    sound.play()
    colorsList2[index] = b.get_color()
    drawButtons(buttons)
    pygame.display.update()
    sleep(500)
    b.set_color(b.COLOR_CONST)
    drawButtons(buttons)


def gameOver(score):
    font = pygame.font.SysFont("Arial", 60, "bold")
    font2 = pygame.font.SysFont("Arial", 40)

    while True:
        window.fill((0, 0, 0))

        window.blit(font.render("GAME OVER", True, (255, 255, 255)), (80, 20))
        window.blit(font2.render(f"SCORE: {score}", True, (255, 255, 255)), (170, 150))

        menuButton = pygame.draw.rect(window, BUTTON_COLOR, (150, 300, 200, 80))
        window.blit(font.render("Menu", True, (255, 255, 255)), (175, 305))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menuButton.collidepoint(event.pos):
                    menu()

        pygame.display.update()



def main():
    colorsList = [(0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 0, 255)]
    neonColorsList = ["#b7ffc3", "#ff9d9f", "#f5ffa1", "#8ee1fd"]

    buttons = createButtons(colorsList)

    font = pygame.font.SysFont("Arial", 30, "bold")
    clock = pygame.time.Clock()
    clickingEnabled = False
    sequence = []
    count = 0
    score = 0
    index = 0
    while True:
        count += 1
        window.fill((0, 0, 0))

        window.blit(simonLogo, (70, 20))

        clock.tick(30)

        window.blit(font.render(f"SCORE: {score}", True, (255, 255, 255)), (20, 450))

        drawButtons(buttons)

        if not clickingEnabled and count > 1:
            sleep(500)
            sequence.append(random.choice(buttons))

            colorsList2 = colorsList.copy()
            for b in sequence:
                buttonPressed(colorsList, colorsList2, b, buttons, neonColorsList)
            clickingEnabled = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if clickingEnabled:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            colorsList2 = colorsList.copy()
                            buttonPressed(colorsList, colorsList2, button, buttons, neonColorsList)

                            if sequence[index] == button:
                                index += 1
                            else:
                                gameOver(score)

                            if index == len(sequence):
                                score += 1
                                clickingEnabled = False
                                index = 0

        pygame.display.update()


if __name__ == "__main__":
    menu()
