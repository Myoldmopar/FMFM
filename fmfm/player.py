from fmfm.circleentity import CircleEntity


class Player(CircleEntity):
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 255, 0))
        self.hp = 10
        self.max_hp = 10
        self.gold = 0
        self.inventory = []
        self.level = 1
        self.exp = 0
        self.name = "Hero"

    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 10:
            self.exp -= self.level * 10
            self.level += 1
            self.max_hp += 2
            self.hp = self.max_hp

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
