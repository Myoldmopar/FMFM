import pygame

from fmfm.scenes.battle import FightScene
from fmfm.scenes.overworld import OverworldScene
from fmfm.scenes.manager import Scene
from fmfm.player import Player
from fmfm.enemy import Enemy
from fmfm.sound import SoundManager


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.running = True

        # --- Persistent game state ---
        self.player = Player(100, 100)
        self.enemies = [
            Enemy(300, 200),
            Enemy(400, 300)
        ]
        self.current_enemy: Enemy | None = None

        # Initialize all sound assets and management
        self.sound = SoundManager()

        # start in the overworld scene
        self.current_scene = OverworldScene(self)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            self.current_scene.handle_event(event)
        return True

    def update(self, dt):
        self.current_scene.update(dt)

    def draw(self):
        self.current_scene.draw(self.screen)
        pygame.display.flip()

    def change_scene(self, new_scene: Scene):
        if new_scene == Scene.Overworld:
            self.current_scene = OverworldScene(self)
        elif new_scene == Scene.Battle:
            self.current_scene = FightScene(self)
        else:
            raise NotImplementedError("Could not instantiate scene with type:" + str(new_scene))
