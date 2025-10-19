import json

from fmfm.tile import Tile


class TileMap:
    def __init__(self, filename=None):
        self.tiles: list[Tile] = []
        if filename:
            self.load_from_file(filename)

    def load_from_file(self, filename):
        with open(filename) as f:
            data = json.load(f)
        for y, row in enumerate(data["map"]):
            for x, cell in enumerate(row):
                if cell == "W":
                    self.tiles.append(Tile(x, y, "wall", solid=True))
                elif cell == "~":
                    self.tiles.append(Tile(x, y, "water", solid=True))
                else:
                    self.tiles.append(Tile(x, y, "grass", solid=False))

    def draw(self, screen, camera):
        for tile in self.tiles:
            tile.draw(screen, camera)

    def is_blocked(self, grid_x, grid_y):
        for tile in self.tiles:
            if tile.x == grid_x and tile.y == grid_y and tile.solid:
                return True
        return False
