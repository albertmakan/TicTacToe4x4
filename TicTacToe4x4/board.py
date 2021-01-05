import random
X, O, E = -1, 1, 0  # values of signs (x, o, empty)


class Board:
    def __init__(self):
        self.squares = [4 * [E], 4 * [E], 4 * [E], 4 * [E]]
        self.row_sums = 4*[0]   # sum of signs in each row
        self.col_sums = 4*[0]   # sum of signs in each column
        self.diag_sums = 2*[0]  # sum of signs in both diagonals
        self.sqr_sums = 9*[0]   # sum of signs in each 2x2 square
        self.x_or_o = X

    def is_full(self):
        for i in range(4):
            for j in range(4):
                if self.squares[i][j] == E:
                    return False
        return True

    def draw_XO(self, row: int, col: int):
        if self.squares[row][col] != E:
            return False
        self.squares[row][col] = self.x_or_o
        self._update_sums(row, col)
        self.x_or_o = -self.x_or_o
        return True

    def _update_sums(self, row: int, col: int):
        xo = self.squares[row][col]
        self.row_sums[row] += xo
        self.col_sums[col] += xo
        if row == col:
            self.diag_sums[0] += xo
        elif row + col == 3:
            self.diag_sums[1] += xo
        for i in range(3):
            for j in range(3):
                self.sqr_sums[i * 3 + j] = self.squares[i][j] + \
                                              self.squares[i + 1][j] + \
                                              self.squares[i][j + 1] + \
                                              self.squares[i + 1][j + 1]

    def reset(self):
        for i in range(4):
            for j in range(4):
                self.squares[i][j] = E
        for i in range(4):
            self.row_sums[i] = 0
            self.col_sums[i] = 0
        self.diag_sums[0] = 0
        self.diag_sums[1] = 0
        for i in range(9):
            self.sqr_sums[i] = 0
        self.x_or_o = X

    def check_win(self):
        max_vals = [
            max(self.row_sums, key=abs), max(self.col_sums, key=abs),
            max(self.diag_sums, key=abs), max(self.sqr_sums, key=abs)]
        max_val = max(max_vals, key=abs)
        if abs(max_val) == 4:
            winner = 'O' if max_val == 4 else 'X'
            if max_vals[0] == max_val:
                return winner, 'r', self.row_sums.index(max_val)
            if max_vals[1] == max_val:
                return winner, 'c', self.col_sums.index(max_val)
            if max_vals[2] == max_val:
                return winner, 'd', self.diag_sums.index(max_val)
            if max_vals[3] == max_val:
                return winner, 's', self.sqr_sums.index(max_val)
        return None

    def _get_advice(self):
        advice = []
        max_val = max([
            max(self.row_sums), max(self.col_sums),
            max(self.diag_sums), max(self.sqr_sums)])
        min_val = min([
            min(self.row_sums), min(self.col_sums),
            min(self.diag_sums), min(self.sqr_sums)])
        if max_val == abs(min_val):
            val_to_find = max_val if self.x_or_o == O else min_val
        else:
            val_to_find = max_val if max_val > abs(min_val) else min_val
        if val_to_find == 0:
            return advice
        for i in range(4):
            if self.row_sums[i] == val_to_find:
                advice.append(("r", i))
            if self.col_sums[i] == val_to_find:
                advice.append(("c", i))
        for i in range(2):
            if self.diag_sums[i] == val_to_find:
                advice.append(("d", i))
        for i in range(9):
            if self.sqr_sums[i] == val_to_find:
                advice.append(("s", i))
        return advice

    def computers_turn(self):
        advice = self._get_advice()
        possible_coord = []
        if len(advice) == 0:
            possible_coord.append((random.randint(1, 2), random.randint(1, 2)))
        for a in advice:
            place, idx = a
            if place == 'r':
                elems = [self.squares[idx][i] for i in range(4)]
                if X in elems and O in elems:
                    continue
                for i in range(4):
                    if self.squares[idx][i] == E:
                        possible_coord.append((idx, i))
            elif place == 'c':
                elems = [self.squares[i][idx] for i in range(4)]
                if X in elems and O in elems:
                    continue
                for i in range(4):
                    if self.squares[i][idx] == E:
                        possible_coord.append((i, idx))
            elif place == 'd':
                if idx == 0:
                    elems = [self.squares[i][i] for i in range(4)]
                    if X in elems and O in elems:
                        continue
                    for i in range(4):
                        if self.squares[i][i] == E:
                            possible_coord.append((i, i))
                else:
                    elems = [self.squares[i][3-i] for i in range(4)]
                    if X in elems and O in elems:
                        continue
                    for i in range(4):
                        if self.squares[i][3-i] == E:
                            possible_coord.append((i, 3-i))
            elif place == 's':
                i, j = idx // 3, idx % 3
                elems = [self.squares[i][j], self.squares[i+1][j], self.squares[i][j+1], self.squares[i+1][j+1]]
                if X in elems and O in elems:
                    continue
                if self.squares[i][j] == E:
                    possible_coord.append((i, j))
                if self.squares[i+1][j] == E:
                    possible_coord.append((i+1, j))
                if self.squares[i][j+1] == E:
                    possible_coord.append((i, j+1))
                if self.squares[i+1][j+1] == E:
                    possible_coord.append((i+1, j+1))
        if len(possible_coord) == 0:
            for i in range(4):
                for j in range(4):
                    if self.squares[i][j] == E:
                        possible_coord.append((i, j))
        i, j = random.choice(possible_coord)
        self.draw_XO(i, j)
        return i, j
