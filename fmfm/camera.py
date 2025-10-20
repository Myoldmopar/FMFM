from fmfm.location import GenericXY


class Camera:
    def __init__(self, width: int, height: int):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def follow(self, target: GenericXY) -> None:
        # Center camera on target
        self.x = target.x - self.width // 2
        self.y = target.y - self.height // 2

    def world_to_screen(self, x: float, y: float) -> tuple[int, int]:
        return int(x - self.x), int(y - self.y)
