from fmfm.tile import GRID_SIZE


class GenericXY:
    def __init__(self, x: int | float, y: int | float):
        self.x = x
        self.y = y


class GridIndexes(GenericXY):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)


class ActualPosition(GenericXY):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    @classmethod
    def from_grid_indexes(cls, grid_indexes: GridIndexes, grid_size: int = GRID_SIZE) -> 'ActualPosition':
        return cls(
            x=grid_indexes.x * grid_size + grid_size / 2,
            y=grid_indexes.y * grid_size + grid_size / 2
        )
