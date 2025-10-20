import pygame

from fmfm.enemy import OverworldEnemy
from fmfm.scenes.base import SceneBase, SceneType
from fmfm.scenes.battle import FightScene
from fmfm.scenes.overworld import OverworldScene
from fmfm.player import Player
from fmfm.sound import SoundManager


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.running = True

        # --- Persistent game state ---
        self.player = Player()

        # Initialize all sound assets and management
        self.sound = SoundManager()

        # We will hold IDs of the current enemies being battled here to pass info back to overworld after the battle
        self.overworld_enemies: dict[int, OverworldEnemy] = {}
        self.current_enemies: list[int] = []

        # start in the overworld scene
        self.loaded_scenes: dict[SceneType, SceneBase] = {}
        self.current_scene: SceneBase | None = None
        self.change_scene(SceneType.Overworld)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            if self.current_scene:
                self.current_scene.handle_event(event)
        return True

    def update(self, dt) -> None:
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self) -> None:
        if self.current_scene:
            self.current_scene.draw(self.screen)
        pygame.display.flip()

    def change_scene(self, new_scene: SceneType) -> None:
        if new_scene == SceneType.Overworld:
            if new_scene not in self.loaded_scenes:
                self.loaded_scenes[new_scene] = OverworldScene(self)
        elif new_scene == SceneType.Battle:
            if new_scene not in self.loaded_scenes:
                self.loaded_scenes[new_scene] = FightScene(self)
        else:
            raise NotImplementedError("Could not instantiate scene with type:" + str(new_scene))
        self.current_scene = self.loaded_scenes[new_scene]
        self.current_scene.re_enter()
