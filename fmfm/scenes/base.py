from abc import ABC, abstractmethod
from enum import Enum


class SceneBase(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def re_enter(self):
        pass


class SceneType(Enum):
    Overworld = "overworld"
    Battle = "battle"
    Shop = "shop"
