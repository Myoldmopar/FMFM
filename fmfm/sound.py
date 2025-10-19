from enum import Enum
from pathlib import Path

import pygame


class Song(Enum):
    Overworld = "overworld"
    Battle = "battle"


class SoundEffect(Enum):
    Attack = "attack"
    Bonk = "bonk"
    Win = "win"


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.assets_path = Path(__file__).parent / "assets"
        self.sounds = self.load_sound()
        self.music_tracks = self.load_music()
        self.music_tracks = {}
        self.current_music = None

    def load_sound(self) -> dict[SoundEffect, pygame.mixer.Sound]:
        sounds = {
            SoundEffect.Attack: pygame.mixer.Sound(self.assets_path / "sounds" / "sword.wav"),
            SoundEffect.Bonk: pygame.mixer.Sound(self.assets_path / "sounds" / "bonk.mp3"),
            SoundEffect.Win: pygame.mixer.Sound(self.assets_path / "sounds" / "melee.wav"),
        }
        return sounds

    def play_sound(self, name) -> None:
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def load_music(self) -> dict[Song, Path]:
        music = {
            Song.Overworld: self.assets_path / "music" / "overworld_theme.ogg",
            Song.Battle: self.assets_path / "music" / "fight.wav",
        }
        return music

    def play_music(self, name: Song, loop: int = -1) -> None:
        """Loop = -1 plays indefinitely"""
        path = self.music_tracks.get(name)
        if path and self.current_music != name:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loop)
            self.current_music = name

    def stop_music(self) -> None:
        pygame.mixer.music.stop()
        self.current_music = None
