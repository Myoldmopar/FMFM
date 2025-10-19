import pygame


class Controls:
    def __init__(self):
        self.keys = pygame.key.get_pressed()

    def update(self):
        self.keys = pygame.key.get_pressed()

    def move_input(self):
        dx, dy = 0, 0
        if self.keys[pygame.K_UP]:
            dy = -1
        if self.keys[pygame.K_DOWN]:
            dy = 1
        if self.keys[pygame.K_LEFT]:
            dx = -1
        if self.keys[pygame.K_RIGHT]:
            dx = 1
        return dx, dy
