import pygame
import os
import random
import math

pygame.init()

wid = 600
hid = 600
screen = pygame.display.set_mode((wid, hid))


def writetex(text, x, y, size):
    cz = pygame.font.SysFont("Courier New", size)
    rend = cz.render(text, 1, (255, 100, 100))
    screen.blit(rend, (x, y))


whatwesee = "menu"


class Obstacle():
    def __init__(self, x, width):
        self.x = x
        self.width = width
        self.y_up = 0
        self.hid_up = random.randint(150, 250)
        self.intersp = 200
        self.y_down = self.hid_up + self.intersp
        self.hid_down = hid - self.y_down
        self.color = (100, 20, 10)
        self.shape_up = pygame.Rect(self.x, self.y_up, self.width, self.hid_up)
        self.shape_down = pygame.Rect(self.x, self.y_down, self.width, self.hid_down)

    def drawing(self):
        pygame.draw.rect(screen, self.color, self.shape_up, 0)
        pygame.draw.rect(screen, self.color, self.shape_down, 0)

    def move(self, v):
        self.x = self.x - v
        self.shape_up = pygame.Rect(self.x, self.y_up, self.width, self.hid_up)
        self.shape_down = pygame.Rect(self.x, self.y_down, self.width, self.hid_down)

    def collision(self, player):
        if self.shape_up.colliderect(player) or self.shape_down.colliderect(player):
            return True
        else:
            return False


class SpaceShip():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 50
        self.width = 50
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.graphics = pygame.image.load(os.path.join('spaceship.png'))

    def drawing(self):
        screen.blit(self.graphics, (self.x, self.y))

    def move(self, v):
        self.y = self.y + v
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
# TODO: List of highscore

obstacle = []

for i in range(21):
    obstacle.append(Obstacle(i * wid / 20, wid / 20))

player = SpaceShip(250, 275)

dy = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -1 / 4
            if event.key == pygame.K_DOWN:
                dy = 1 / 4
            if event.key == pygame.K_SPACE:
                if whatwesee != "game":
                    player = SpaceShip(250, 275)
                    dy = 0
                    whatwesee = "game"
                    points = 0
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    screen.fill((50, 30, 0))

    if whatwesee == "menu":
        writetex("Press" + " "*7 + "to play", 110, 350, 30)
        graphicsspace = pygame.image.load(os.path.join('keySpace.png'))
        screen.blit(graphicsspace, (205, 330))
        writetex("- move UP", 160, 420, 20)
        writetex("- move DOWN", 160, 470, 20)
        graphics = pygame.image.load(os.path.join('spaceshipbig.png'))
        graphicsup = pygame.image.load(os.path.join('moveUp.png'))
        graphicsdown = pygame.image.load(os.path.join('moveDown.png'))
        screen.blit(graphicsup, (100, 400))
        screen.blit(graphicsdown, (100, 450))
        screen.blit(graphics, (180, 80))

    elif whatwesee == "game":
        # TODO: Start without moving obstacle
        # TODO: Space without fire from beginning
        # TODO: Make speeding

        for p in obstacle:
            p.move(1)
            p.drawing()
            if p.collision(player.shape):
                whatwesee = "End"
        for p in obstacle:
            if p.x <= -p.width:
                obstacle.remove(p)
                obstacle.append((Obstacle(wid, wid / 20)))
                points = points + math.fabs(dy)

        player.move(dy)
        player.drawing()
        writetex(str(points), 50, 50, 20)

    elif whatwesee == "End":
        graphics = pygame.image.load(os.path.join('spaceshipbig.png'))
        screen.blit(graphics, (180, 80))
        writetex("Unfortunately you lose", 100, 300, 30)
        writetex("Your score is: " + str(points), 150, 350, 20)
        writetex("Press" + " "*9 + "to play again", 150, 400, 20)
        graphicsspace = pygame.image.load(os.path.join('keySpace.png'))
        screen.blit(graphicsspace, (210, 370))
        graphicsesc = pygame.image.load(os.path.join('keyEsc.png'))
        screen.blit(graphicsesc, (220, 450))
        writetex("Press" + " "*6 + "to end the game", 150, 470, 20)

    pygame.display.update()