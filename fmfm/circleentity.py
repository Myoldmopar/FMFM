import pygame


class CircleEntity:
    def __init__(self, x, y, color=(255, 255, 255), radius=10):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.draw_me = True

    def draw(self, surface, camera):
        if not self.draw_me:
            return
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        pygame.draw.circle(surface, self.color, (screen_x, screen_y), self.radius)
