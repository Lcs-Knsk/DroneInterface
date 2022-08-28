import pygame

class Button():
    def __init__(self, x, y, imgDown, imgUp, ButtonWidth):
        self.x = x
        self.y = y
        self.keyDown = False
        self.img = pygame.image.load(imgDown)
        self.img = pygame.transform.scale(self.img, (ButtonWidth, ButtonWidth))

        self.imgDown = pygame.image.load(imgUp)
        self.imgDown = pygame.transform.scale(self.imgDown, (ButtonWidth, ButtonWidth))

        self.backgroundColor = (100, 90, 100)
        self.highlightColor = (70, 70, 70)
        self.borderColor = (0, 255, 0)

        self.width = ButtonWidth
        self.height = ButtonWidth
