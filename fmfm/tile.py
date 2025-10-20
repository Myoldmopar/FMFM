import pygame

from fmfm.geometry import GRID_TILE_SIZE


class Tile:
    def __init__(self, x, y, tile_type="grass", solid=False):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.solid = solid

    def draw(self, screen, camera):
        color = (100, 200, 100)
        if self.tile_type == "water":
            color = (50, 100, 200)
        elif self.tile_type == "wall":
            color = (80, 80, 80)
        elif self.tile_type == "grass":
            color = (100, 200, 100)
        screen_x = self.x * GRID_TILE_SIZE - GRID_TILE_SIZE // 2 - camera.x
        screen_y = self.y * GRID_TILE_SIZE - GRID_TILE_SIZE // 2 - camera.y
        pygame.draw.rect(screen, color, (screen_x, screen_y, GRID_TILE_SIZE, GRID_TILE_SIZE))
