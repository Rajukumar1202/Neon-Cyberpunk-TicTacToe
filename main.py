
import pygame
import sys

from game import TicTacToe
from ui import (
    draw_game,
    handle_click,
    handle_ai_move,
    AI_MOVE_EVENT
)

WIDTH, HEIGHT = 720, 820
FPS = 60


def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic-Tac-Toe | Python Quest 2.0")

    clock = pygame.time.Clock()

    game = TicTacToe()

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    handle_click(event.pos, game)

            elif event.type == AI_MOVE_EVENT:

                handle_ai_move(game)

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    pygame.time.set_timer(AI_MOVE_EVENT, 0)
                    game.new_round()

                elif event.key == pygame.K_ESCAPE:
                    running = False

        draw_game(screen, game)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
