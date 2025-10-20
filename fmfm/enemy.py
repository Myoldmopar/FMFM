import pygame

from fmfm.location import GenericXY


class OverworldEnemy:
    def __init__(self, x: int, y: int, radius: int = 10, color: tuple[int, int, int] = (200, 50, 50), speed: int = 1):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.speed = speed
        self.alive = True
        self.is_threat = True

    def update(self, target: GenericXY | None = None):
        if not self.alive:
            return
        if not self.is_threat:
            self.color = (100, 100, 100)
            return
        # Basic follow behavior if target is provided
        # TODO: Maybe just wander if no target provided?
        if target is not None:
            dx = target.x - self.x
            dy = target.y - self.y
            dist = max((dx ** 2 + dy ** 2) ** 0.5, 1)
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

    def draw(self, surface, camera):
        if not self.alive:
            return
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        pygame.draw.circle(surface, self.color, (screen_x, screen_y), self.radius)
