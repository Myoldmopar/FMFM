import pygame

from fmfm.camera import Camera
from fmfm.location import ActualPosition, GridIndexes


class OverworldData:
    def __init__(self, x: int, y: int, color: tuple[int, int, int], radius: int):
        self.xy_grid = GridIndexes(x, y)
        self.xy_world = ActualPosition.from_grid_indexes(self.xy_grid)
        self.color = color
        self.radius = radius


class Player:
    def __init__(self):
        self.overworld_data: OverworldData | None = None

    def add_overworld_data(self, x: int, y: int, color: tuple[int, int, int] = (255, 255, 255), radius: int = 10):
        self.overworld_data = OverworldData(x, y, color, radius)

    def draw_overworld(self, surface: pygame.Surface, camera: Camera):
        screen_x, screen_y = camera.world_to_screen(self.overworld_data.xy_world.x, self.overworld_data.xy_world.y)
        pygame.draw.circle(surface, self.overworld_data.color, (screen_x, screen_y), self.overworld_data.radius)
