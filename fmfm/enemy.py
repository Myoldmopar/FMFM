from fmfm.circleentity import CircleEntity


class Enemy(CircleEntity):
    def __init__(self, x, y, radius=10, color=(200, 50, 50), hp=10, speed=1):
        super().__init__(x, y, color, radius)
        self.hp = hp
        self.speed = speed
        self.alive = True
        self.is_threat = True

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def update(self, player):
        if not self.alive:
            self.draw_me = False
            return
        if not self.is_threat:
            self.color = (100, 100, 100)
            return
        # Basic follow behavior
        dx = player.x - self.x
        dy = player.y - self.y
        dist = max((dx**2 + dy**2) ** 0.5, 1)
        self.x += self.speed * dx / dist
        self.y += self.speed * dy / dist
