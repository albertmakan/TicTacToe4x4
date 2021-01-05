import pygame as pg
from board import Board, X, O


class TicTacToeWindow:
    def __init__(self):
        pg.init()
        self.w = 400
        self.h = 400
        self.screen = pg.display.set_mode((self.w, self.h + 100), 0, 32)
        pg.display.set_caption("Tic Tac Toe 4x4")
        self.x_img = pg.image.load("x.jpg")
        self.o_img = pg.image.load("o.jpg")
        self.board = Board()
        self.message = ""
        self.compX = False
        self.game_over = False
        self._reset_screen()

    def _reset_screen(self):
        self.screen.fill((255, 255, 255))
        for i in range(1, 4):
            pg.draw.line(self.screen, (0, 0, 0), (i * self.w / 4, 0), (i * self.w / 4, self.h), 7)
            pg.draw.line(self.screen, (0, 0, 0), (0, i * self.h / 4), (self.w, i * self.h / 4), 7)

    def init_message(self):
        if self.compX:
            self.message = "Computer's turn."
        else:
            self.message = "Your turn. Place an X somewhere."
        self._draw_message()

    def _draw_message(self):
        font = pg.font.Font(None, 30)
        text = font.render(self.message, True, (255, 255, 255))
        self.screen.fill((0, 0, 0), (0, 400, 500, 100))
        text_rect = text.get_rect(center=(self.w / 2, 500 - 50))
        self.screen.blit(text, text_rect)
        pg.display.update()

    def _draw_XO(self, row: int, col: int):
        pos_y = row * self.w / 4 + 10
        pos_x = col * self.h / 4 + 10
        if self.board.x_or_o == O:
            self.screen.blit(self.x_img, (pos_x, pos_y))
        else:
            self.screen.blit(self.o_img, (pos_x, pos_y))
        self._check_result()

    def _check_result(self):
        result = self.board.check_win()
        if result:
            winner, place, idx = result
            if (winner == 'X' and self.compX) or (winner == 'O' and not self.compX):
                self.message = "Computer wins! Click here to restart"
            else:
                self.message = "You win! Click here to restart"
            if place == 'r':
                pg.draw.line(self.screen, (250, 0, 0),
                             (0, (idx + 1) * self.h / 4 - self.h / 8),
                             (self.w, (idx + 1) * self.h / 4 - self.h / 8),
                             6)
            elif place == 'c':
                pg.draw.line(self.screen, (250, 0, 0),
                             ((idx + 1) * self.w / 4 - self.w / 8, 0),
                             ((idx + 1) * self.w / 4 - self.w / 8, self.h),
                             6)
            elif place == 'd':
                pg.draw.line(self.screen, (250, 0, 0),
                             (0 if idx == 0 else self.w, 0),
                             (self.w if idx == 0 else 0, self.h),
                             6)
            elif place == 's':
                left_top = ((idx % 3) * self.w / 4, (idx // 3) * self.h / 4 + self.h / 8)
                pg.draw.line(self.screen, (250, 0, 0),
                             left_top,
                             (left_top[0] + self.w / 2, left_top[1]),
                             6)
                pg.draw.line(self.screen, (250, 0, 0),
                             (left_top[0], left_top[1] + self.h / 4),
                             (left_top[0] + self.w / 2, left_top[1] + self.h / 4),
                             6)
            self.game_over = True
        elif self.board.is_full():
            self.message = "Game Draw! Click here to restart"
            self.game_over = True
        else:
            if (self.compX and self.board.x_or_o == X) or (not self.compX and self.board.x_or_o == O):
                self.message = "Computer's turn."
            else:
                self.message = "Your turn. Place an "+('X' if self.board.x_or_o == X else 'O')+" somewhere."
        self._draw_message()
        pg.display.update()

    def computers_answer(self):
        row, col = self.board.computers_turn()
        self._draw_XO(row, col)

    def player_click(self):
        pos_x, pos_y = pg.mouse.get_pos()
        row, col = None, None
        if pos_x < self.w / 4:
            col = 0
        elif pos_x < self.w / 2:
            col = 1
        elif pos_x < self.w / 4 * 3:
            col = 2
        elif pos_x < self.w:
            col = 3
        if pos_y < self.h / 4:
            row = 0
        elif pos_y < self.h / 2:
            row = 1
        elif pos_y < self.h / 4 * 3:
            row = 2
        elif pos_y < self.h:
            row = 3
        if not (row is None or col is None):
            if self.board.draw_XO(row, col):
                self._draw_XO(row, col)
                return True
        return False

    def reset(self):
        self.board.reset()
        self.message = ""
        self._reset_screen()
        self.game_over = False
