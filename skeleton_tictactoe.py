#!/usr/bin/env pypy

import time


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, recommend=True):
        self.get_parameters()
        self.initialize_game()
        self.recommend = recommend

    def initialize_game(self):
        self.current_state = [['.' for x in range(self.n)] for y in range(self.n)]

        # Player X always plays first
        self.player_turn = 'X'

    def draw_board(self):
        print()
        for y in range(0, self.n):
            for x in range(0, self.n):
                print(F'{self.current_state[x][y]}', end="")
            print()
        print()

    def is_valid(self, px, py):
        if px < 0 or px > self.n - 1 or py < 0 or py > self.n - 1:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):
        # Column win
        for column in self.current_state:
            current = column[0]
            count = 0
            for i in range(len(column)):
                if column[i] == '.':
                    count = 0
                elif current != column[i]:
                    count = 1
                elif column[i] == current:
                    count += 1
                current = column[i]
                if count == self.s:
                    return current

        # Horizontal win
        for i in range(self.n):
            count = 0
            current = self.current_state[0][i]
            for column in self.current_state:
                if column[i] == '.':
                    count = 0
                elif current != column[i]:
                    count = 1
                elif current == column[i]:
                    count += 1
                current = column[i]
                if count == self.s:
                    return current

        mat = [[0, 1, 2, 3, 9],
               [4, 5, 6, 7, 0],
               [8, 9, 10, 11, 18],
               [1, 2, 3, 7, 0],
               [4, 8, 5, 7, 10]]

        diagonals = []
        for start in range(self.n):
            for j in range(self.n - self.s + 1):
                diagonal = [self.current_state[start + i][i + j] for i in range(self.s) if
                            0 <= i + j < self.n and 0 <= start + i < self.n]
                if len(diagonal) >= self.s:
                    diagonals.append(diagonal)
                diagonal = [self.current_state[start + i][-i - j - 1] for i in range(self.s) if
                            0 <= i + j < self.n and 0 <= start + i < self.n]
                if len(diagonal) >= self.s:
                    diagonals.append(diagonal)

        for diag in diagonals:
            first = diag[0]
            if first == '.':
                break
            for i in range(len(diag)):
                if first != diag[i]:
                    break
                if i == len(diag)-1:
                    return diag[i]

        # Is whole board full?
        for i in range(self.n):
            for j in range(self.n):
                # There's an empty field, we continue the game
                if self.current_state[i][j] == '.':
                    return None
        # It's a tie!
        return '.'

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is X!')
            elif self.result == 'O':
                print('The winner is O!')
            elif self.result == '.':
                print("It's a tie!")
            self.initialize_game()
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    def minimax(self, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax(max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    def alphabeta(self, alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(self.n):
            for j in range(self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(alpha, beta, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value
        return (value, x, y)

    def play(self):
        if self.a:
            algo = self.ALPHABETA
        else:
            algo = self.MINIMAX

        if self.player1_type == 'H':
            player_x = self.HUMAN
        else:
            player_x = self.AI

        if self.player2_type == 'H':
            player_o = self.HUMAN
        else:
            player_o = self.AI

        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(max=False)
                else:
                    (_, x, y) = self.minimax(max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(max=False)
                else:
                    (m, x, y) = self.alphabeta(max=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()

    def get_parameters(self):
        self.n = int(input('Enter size of board (n): '))
        while self.n < 3 or self.n > 10:
            self.n = str(input('Please enter a number between 3 and 10 for n: '))

        self.b = int(input('Enter the number of blocs (b): '))
        while self.b > 2 * self.n or self.b < 0:
            self.b = input('Please enter a number between 0 and' + str(2 * self.n) + ' for b: ')

        self.b_positions = []
        for i in range(self.b):
            x = int(input('Enter the x coordinate of b ' + str(i + 1) + ': '))
            y = int(input('Enter the y coordinate:of b ' + str(i + 1) + ': '))
            self.b_positions.append((x, y))

        self.s = int(input('Enter the winning line-up size (s): '))
        while self.s < 3 or self.s > 10:
            self.s = int(input('Please enter a number between 3 and 10 for s: '))

        self.d1 = int(input('Enter the maximum depth of the adversarial search for player 1 (d1): '))
        self.d2 = int(input('Enter the maximum depth of the adversarial search for player 2 (d2): '))

        self.t = int(input('Enter the maximum allowed time (in seconds) to return a move: '))

        mini_or_alpha = int(input('Enter 1 to use minimax or 2 to sue alphabeta: '))
        while mini_or_alpha != 1 and mini_or_alpha != 2:
            mini_or_alpha = int(input('Enter 1 to use minimax or 2 to sue alphabeta: '))
        if mini_or_alpha == 1:
            self.a = False
        else:
            self.a = True

        self.player1_type = input('Enter H or AI for player 1: ')
        self.player2_type = input('Enter H or AI for player 2: ')


def main():
    g = Game(recommend=True)
    g.play()


if __name__ == "__main__":
    main()
