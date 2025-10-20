class Camera:
    def __init__(self, width: int, height: int):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def follow(self, target_x: int, target_y: int) -> None:
        # Center camera on target
        self.x = target_x - self.width // 2
        self.y = target_y - self.height // 2

    def world_to_screen(self, x: float, y: float) -> tuple[int, int]:
        return int(x - self.x), int(y - self.y)
