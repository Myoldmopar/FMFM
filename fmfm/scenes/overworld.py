from random import randrange

import pygame

from fmfm.camera import Camera
from fmfm.controls import Controls
from fmfm.enemy import OverworldEnemy
from fmfm.scenes.base import SceneBase
from fmfm.scenes.enums import Scene
from fmfm.sound import Song, SoundEffect
from fmfm.tilemap import TileMap
from fmfm.tile import GRID_SIZE

MOVE_SPEED = 200


class OverworldScene(SceneBase):
    def __init__(self, game):
        super().__init__(game)
        self.player = self.game.player
        self.player.add_overworld_data(0, 0, (200, 200, 255), 10)
        self.game.overworld_enemies = {
            randrange(1, 2**80): OverworldEnemy(300, 200),
            randrange(1, 2**80): OverworldEnemy(400, 300)
        }
        self.camera = Camera(800, 600)
        self.controls = Controls()
        self.debug_grid = True
        self.moving = False
        self.move_target = (self.player.overworld_data.xy_world.x, self.player.overworld_data.xy_world.y)
        self.game.sound.play_music(Song.Overworld)
        self.map = TileMap("overworld.json")

    def re_enter(self):
        self.game.sound.play_music(Song.Overworld)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                self.debug_grid = not self.debug_grid

    def update(self, dt):

        self.controls.update()

        if self.moving:
            self._update_movement(dt)
        else:
            dx, dy = self.controls.move_input()
            if dx != 0 or dy != 0:
                target_x = self.player.overworld_data.xy_world.x + dx * GRID_SIZE
                target_y = self.player.overworld_data.xy_world.y + dy * GRID_SIZE
                if self.map.is_blocked(target_x // GRID_SIZE, target_y // GRID_SIZE):
                    self.game.sound.play_sound(SoundEffect.Bonk)
                else:
                    self.move_target = (target_x, target_y)
                    self.moving = True

        self.camera.follow(self.player.overworld_data.xy_world)

        # Update enemies, detect collision -> trigger battle
        for enemy_id, enemy in self.game.overworld_enemies.items():
            enemy.update(self.player.overworld_data.xy_world)
            if enemy.is_threat and enemy.alive:
                dx = enemy.x - self.player.overworld_data.xy_world.x
                dy = enemy.y - self.player.overworld_data.xy_world.y
                if (dx ** 2 + dy ** 2) ** 0.5 < enemy.radius + self.player.overworld_data.radius:
                    self.game.current_enemies = [enemy_id]
                    self.game.change_scene(Scene.Battle)
                    (self.player.x, self.player.y) = self.move_target

    def _update_movement(self, dt):
        x, y = self.player.overworld_data.xy_world.x, self.player.overworld_data.xy_world.y
        tx, ty = self.move_target
        dx, dy = tx - x, ty - y
        dist = (dx**2 + dy**2) ** 0.5
        if dist < 1:
            self.player.overworld_data.xy_world.x, self.player.overworld_data.xy_world.y = tx, ty
            self.moving = False
            return
        move_x = (dx / dist) * MOVE_SPEED * dt
        move_y = (dy / dist) * MOVE_SPEED * dt
        if abs(move_x) > abs(dx):
            move_x = dx
        if abs(move_y) > abs(dy):
            move_y = dy
        self.player.overworld_data.xy_world.x += move_x
        self.player.overworld_data.xy_world.y += move_y

    def draw(self, surface):
        surface.fill((30, 30, 40))
        self.map.draw(surface, self.camera)
        self.player.draw_overworld(surface, self.camera)
        for enemy_id, enemy in self.game.overworld_enemies.items():
            enemy.draw(surface, self.camera)
        if self.debug_grid:
            self._draw_grid(surface)

    def _draw_grid(self, surface):
        color = (60, 60, 60)
        width, height = surface.get_size()
        start_x = -(self.camera.x % GRID_SIZE)
        start_y = -(self.camera.y % GRID_SIZE)
        for x in range(int(start_x), width, GRID_SIZE):
            pygame.draw.line(surface, color, (x, 0), (x, height))
        for y in range(int(start_y), height, GRID_SIZE):
            pygame.draw.line(surface, color, (0, y), (width, y))
