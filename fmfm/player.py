import pygame

from fmfm.camera import Camera


class Player:
    def __init__(self):
        self.overworld_x = 0
        self.overworld_y = 0
        self.overworld_color = (0, 0, 255)
        self.overworld_radius = 10

    def add_overworld_data(self, x: int, y: int, color: tuple[int, int, int] = (255, 255, 255), radius: int = 10):
        self.overworld_x = x
        self.overworld_y = y
        self.overworld_color = color
        self.overworld_radius = radius

    def draw_overworld(self, surface: pygame.Surface, camera: Camera):
        screen_x, screen_y = camera.world_to_screen(self.overworld_x, self.overworld_y)
        pygame.draw.circle(surface, self.overworld_color, (screen_x, screen_y), self.overworld_radius)
