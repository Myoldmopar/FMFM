import pygame

from fmfm.sound import Song, SoundEffect
from fmfm.scenes.base import SceneBase
from fmfm.scenes.enums import Scene


class FightScene(SceneBase):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 48)
        self.game.sound.play_music(Song.Battle)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            for enemy_id in self.game.current_enemies:
                self.game.overworld_enemies[enemy_id].is_threat = False
            self.game.change_scene(Scene.Overworld)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # "Defeat" the enemy when space is pressed
            self.game.sound.play_sound(SoundEffect.Attack)
            for enemy_id in self.game.current_enemies:
                self.game.overworld_enemies[enemy_id].alive = False
                # self.game.enemies.remove(self.game.current_enemy)
                self.game.sound.play_sound(SoundEffect.Win)
            self.game.change_scene(Scene.Overworld)

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill((80, 0, 0))
        text = self.font.render("Fight Scene! (SPACE to win, ESC to spare)", True, (255, 255, 255))
        surface.blit(text, (100, 100))
