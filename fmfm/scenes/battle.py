import pygame

from fmfm.sound import Song, SoundEffect
from fmfm.scenes.manager import Scene


class FightScene:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.timer = 0
        self.battle_over = False
        self.game.sound.play_music(Song.Battle)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.current_enemy.is_threat = False
            self.game.change_scene(Scene.Overworld)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # "Defeat" the enemy when space is pressed
            self.game.sound.play_sound(SoundEffect.Attack)
            if self.game.current_enemy in self.game.enemies:
                self.game.enemies.remove(self.game.current_enemy)
                self.game.sound.play_sound(SoundEffect.Win)
            self.game.change_scene(Scene.Overworld)

    def update(self, dt):
        self.timer += dt

    def draw(self, surface):
        surface.fill((80, 0, 0))
        text = self.font.render("Fight Scene! (SPACE to win, ESC to spare)", True, (255, 255, 255))
        surface.blit(text, (100, 100))
