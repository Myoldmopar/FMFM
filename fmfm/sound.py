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
        sounds_path = Path(__file__).parent / "assets" / "sounds"
        self.sounds = {
            SoundEffect.Attack: pygame.mixer.Sound(sounds_path / "sword.wav"),
            SoundEffect.Bonk: pygame.mixer.Sound(sounds_path / "bonk.mp3"),
            SoundEffect.Win: pygame.mixer.Sound(sounds_path / "melee.wav"),
        }
        music_path = Path(__file__).parent / "assets" / "music"
        self.music_tracks = {
            Song.Overworld: music_path / "overworld_theme.ogg",
            Song.Battle: music_path / "fight.wav",
        }
        self.current_music = None

    def play_sound(self, name: SoundEffect) -> None:
        self.sounds[name].play()

    def play_music(self, name: Song, loop: int = -1) -> None:
        """Loop = -1 plays indefinitely"""
        path = self.music_tracks[name]
        if self.current_music != name:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loop)
            self.current_music = name

    def stop_music(self) -> None:
        pygame.mixer.music.stop()
        self.current_music = None
