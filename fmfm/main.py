import pygame

from fmfm.game import Game
from fmfm.geometry import GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH


def main():
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))
    pygame.display.set_caption("FM FM")
    clock = pygame.time.Clock()

    game = Game(screen)
    running = True

    while running:
        dt = clock.tick(60) / 1000.0  # delta time in seconds
        running = game.handle_events()
        game.update(dt)
        game.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
