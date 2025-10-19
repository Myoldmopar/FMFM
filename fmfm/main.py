import pygame
from fmfm.game import Game


def main():
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Grid RPG")
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
