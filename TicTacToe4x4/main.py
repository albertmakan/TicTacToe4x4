from window import TicTacToeWindow
import pygame as pg
import sys
import time
from pygame.locals import *
import random

CLOCK = pg.time.Clock()


def game(window):
    window.compX = random.random() < 0.5
    window.init_message()
    if window.compX:
        window.computers_answer()
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                game_over = window.game_over
                if not window.player_click() and not game_over:
                    continue
                if game_over:
                    window.reset()
                    return
                if not window.game_over:
                    time.sleep(0.5)  # simulate thinking
                    window.computers_answer()
        CLOCK.tick(30)


if __name__ == '__main__':
    w = TicTacToeWindow()
    while True:
        game(w)

