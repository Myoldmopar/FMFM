from random import randrange

import pygame

from fmfm.camera import Camera
from fmfm.enemy import OverworldEnemy
from fmfm.geometry import GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH
from fmfm.scenes.base import SceneBase, SceneType
from fmfm.sound import Song, SoundEffect
from fmfm.tilemap import TileMap, TileMapSets
from fmfm.tile import GRID_TILE_SIZE

MOVE_SPEED = 200


class OverworldScene(SceneBase):
    def __init__(self, game):
        super().__init__(game)
        self.game.player.add_overworld_data(0, 0, (200, 200, 255), 10)
        self.game.overworld_enemies = {
            randrange(1, 2**80): OverworldEnemy(300, 200),
            randrange(1, 2**80): OverworldEnemy(400, 300)
        }
        self.camera = Camera(GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT)
        self.debug = True
        self.font = pygame.font.SysFont(None, 28)
        self.moving = False
        self.move_target_x = self.game.player.overworld_x
        self.move_target_y = self.game.player.overworld_y
        self.game.sound.play_music(Song.Overworld)
        self.map = TileMap(TileMapSets.Overworld)

    def re_enter(self):
        self.game.sound.play_music(Song.Overworld)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                self.debug = not self.debug

    def update(self, dt):
        # if we are already moving, continue movement, otherwise check for new movement input
        if self.moving:
            self._update_movement(dt)
        else:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_UP]:
                dy = -1
            if keys[pygame.K_DOWN]:
                dy = 1
            if keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_RIGHT]:
                dx = 1
            if dx != 0 or dy != 0:
                target_x = self.game.player.overworld_x + dx * GRID_TILE_SIZE
                target_y = self.game.player.overworld_y + dy * GRID_TILE_SIZE
                if self.map.is_blocked(target_x // GRID_TILE_SIZE, target_y // GRID_TILE_SIZE):
                    self.game.sound.play_sound(SoundEffect.Bonk)
                else:
                    self.move_target_x = target_x
                    self.move_target_y = target_y
                    self.moving = True

        # make sure camera is updated following any possible movement
        self.camera.follow(self.game.player.overworld_x, self.game.player.overworld_y)

        # Update enemies, detect collision -> trigger battle and go ahead and move player to target position
        for enemy_id, enemy in self.game.overworld_enemies.items():
            enemy.update(self.game.player.overworld_x, self.game.player.overworld_y)
            if enemy.is_threat and enemy.alive:
                dx = enemy.x - self.game.player.overworld_x
                dy = enemy.y - self.game.player.overworld_y
                if (dx ** 2 + dy ** 2) ** 0.5 < enemy.radius + self.game.player.overworld_radius:
                    self.game.current_enemies = [enemy_id]
                    self.game.change_scene(SceneType.Battle)
                    self.game.player.overworld_x = self.move_target_x
                    self.game.player.overworld_y = self.move_target_y

    def _update_movement(self, dt):
        dx, dy = self.move_target_x - self.game.player.overworld_x, self.move_target_y - self.game.player.overworld_y
        dist = (dx**2 + dy**2) ** 0.5
        if dist < 1:
            # close enough, just move to target and stop moving
            self.game.player.overworld_x = self.move_target_x
            self.game.player.overworld_y = self.move_target_y
            self.moving = False
            return
        move_x = (dx / dist) * MOVE_SPEED * dt
        move_y = (dy / dist) * MOVE_SPEED * dt
        if abs(move_x) > abs(dx):
            move_x = dx
        if abs(move_y) > abs(dy):
            move_y = dy
        self.game.player.overworld_x += move_x
        self.game.player.overworld_y += move_y

    def draw(self, surface):
        surface.fill((30, 30, 40))
        self.map.draw(surface, self.camera)
        self.game.player.draw_overworld(surface, self.camera)
        for enemy_id, enemy in self.game.overworld_enemies.items():
            enemy.draw(surface, self.camera)
        if self.debug:
            self.debug_data(surface)
            self.debug_grid(surface)

    def debug_data(self, surface):
        color = (255, 255, 255)
        player = self.game.player
        text = self.font.render("--DEBUG DATA--", True, color)
        surface.blit(text, (500, 10))
        text = self.font.render(
            f"Player Position ({int(player.overworld_x)}, {int(player.overworld_y)})", True, color
        )
        surface.blit(text, (500, 40))
        text = self.font.render(
            f"Player Move Target ({int(self.move_target_x)}, {int(self.move_target_y)})", True, color
        )
        surface.blit(text, (500, 70))

    def debug_grid(self, surface):
        color = (60, 60, 60)
        width, height = surface.get_size()
        start_x = -(self.camera.x % GRID_TILE_SIZE)
        start_y = -(self.camera.y % GRID_TILE_SIZE)
        for x in range(int(start_x), width, GRID_TILE_SIZE):
            pygame.draw.line(surface, color, (x, 0), (x, height))
        for y in range(int(start_y), height, GRID_TILE_SIZE):
            pygame.draw.line(surface, color, (0, y), (width, y))
