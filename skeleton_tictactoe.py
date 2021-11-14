#!/usr/bin/env pypy
import sys
import time


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, recommend=True):
        self.current_state = []
        self.player_turn = ''
        self.get_parameters()
        self.initialize_game()
        self.recommend = recommend
        self.evaluations = {}

    def initialize_game(self):
        self.current_state = [['.' for x in range(self.n)] for y in range(self.n)]
        for b in self.b_positions:
            self.current_state[b[0]][b[1]] = '-'
        # Player X always plays first
        self.player_turn = 'X'

    def draw_board(self):
        print()
        for y in range(0, self.n):
            for x in range(0, self.n):
                print(F'{self.current_state[x][y]}', end="")
            print()
        print()

    def write_board(self):
        self.f.write("\n\n   ")
        for i in range(self.n):
            self.f.write(F"{i}  ")
        self.f.write("\n +-")
        for i in range(self.n):
            self.f.write("---")
        self.f.write("\n")

        for y in range(0, self.n):
            self.f.write(F"{y}|")
            for x in range(0, self.n):
                self.f.write(F" {self.current_state[x][y]} ")
            self.f.write("\n")
        self.f.write("\n")

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
                if column[i] == '.' or column[i] == '-':
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
                if column[i] == '.' or column[i] == '-':
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
                if i == len(diag) - 1:
                    return diag[i]

        # Is whole board full?
        for i in range(self.n):
            for j in range(self.n):
                # There's an empty field, we continue the game
                if self.current_state[i][j] == '.' or self.current_state[i][j] == '-':
                    return None
        # It's a tie!
        return '.'

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is X!')
                self.f.write('The winner is X!')
            elif self.result == 'O':
                print('The winner is O!')
                self.f.write('The winner is O!')
            elif self.result == '.':
                print("It's a tie!")
                self.f.write("It's a tie!")
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

    def minimax(self, max=False, count=0, start=time.time()):
        # count is for the max depth allowed
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        x = None
        y = None

        h_result = sys.maxsize
        if max:
            h_result = -sys.maxsize - 1
        result = self.is_end()

        if result == 'X':
            h_result = self.call_heuristic()
            if count in self.evaluations.keys():
                self.evaluations[count] += 1
            else:
                self.evaluations[count] = 1
            return x, y, h_result
        elif result == 'O':
            h_result = self.call_heuristic()
            if count in self.evaluations.keys():
                self.evaluations[count] += 1
            else:
                self.evaluations[count] = 1
            return x, y, h_result
        elif result == '.':
            h_result = self.call_heuristic()
            if count in self.evaluations.keys():
                self.evaluations[count] += 1
            else:
                self.evaluations[count] = 1
            return x, y, h_result

        if self.player_turn == 'X':
            max_depth = self.d1
        else:
            max_depth = self.d2

        now = time.time()
        if now - start < self.t - 0.005:
            for i in range(self.n):
                for j in range(self.n):
                    if self.current_state[i][j] == '.' and count < max_depth:
                        count += 1
                        # leaf node
                        if count == max_depth - 1:
                            h_result = self.call_heuristic()
                            if count in self.evaluations.keys():
                                self.evaluations[count] += 1
                            else:
                                self.evaluations[count] = 1
                        if max:
                            self.current_state[i][j] = 'O'
                            (_, _, h) = self.minimax(max=False, start=start, count=count)
                            if h >= h_result:
                                h_result = h
                                x = i
                                y = j
                        else:
                            self.current_state[i][j] = 'X'
                            (_, _, h) = self.minimax(max=True, start=start, count=count)
                            if h <= h_result:
                                h_result = h
                                x = i
                                y = j

                        self.current_state[i][j] = '.'
        else:
            h_result = self.call_heuristic()
            if count in self.evaluations.keys():
                self.evaluations[count] += 1
            else:
                self.evaluations[count] = 1
        return x, y, h_result

    def alphabeta(self, alpha=-2, beta=2, max=False, count=0, start=time.time()):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        x = None
        y = None

        h_result = sys.maxsize
        if max:
            h_result = -sys.maxsize - 1

        result = self.is_end()
        if result == 'X':
            h_result = self.call_heuristic()
            if count in self.evaluations.keys():
                self.evaluations[count] += 1
            else:
                self.evaluations[count] = 1
            return x, y, h_result
        elif result == 'O':
            h_result = self.call_heuristic()
            if count in self.evaluations.keys():
                self.evaluations[count] += 1
            else:
                self.evaluations[count] = 1
            return x, y, h_result
        elif result == '.':
            h_result = self.call_heuristic()
            if count in self.evaluations.keys():
                self.evaluations[count] += 1
            else:
                self.evaluations[count] = 1
            return x, y, h_result

        if self.player_turn == 'X':
            max_depth = self.d1
        else:
            max_depth = self.d2

        now = time.time()
        if now - start < self.t - 0.005:
            for i in range(self.n):
                for j in range(self.n):
                    if self.current_state[i][j] == '.' and count < max_depth:
                        count += 1
                        # leaf node
                        if count == max_depth - 1:
                            h_result = self.call_heuristic()
                            if count in self.evaluations.keys():
                                self.evaluations[count] += 1
                            else:
                                self.evaluations[count] = 1
                        if max:
                            self.current_state[i][j] = 'O'
                            (_, _, h) = self.alphabeta(alpha, beta, max=False, start=start, count=count)
                            if h >= h_result:
                                h_result = h
                                x = i
                                y = j
                        else:
                            self.current_state[i][j] = 'X'
                            (_, _, h) = self.alphabeta(alpha, beta, max=True, start=start, count=count)
                            if h <= h_result:
                                h_result = h
                                x = i
                                y = j
                        self.current_state[i][j] = '.'
                        if max:
                            if h_result >= beta:
                                return (x, y, h_result)
                            if h_result > alpha:
                                alpha = h_result
                        else:
                            if h_result <= alpha:
                                return (x, y, h_result)
                            if h_result < beta:
                                beta = h_result
        else:
            h_result = self.call_heuristic()
            if count in self.evaluations.keys():
                self.evaluations[count] += 1
            else:
                self.evaluations[count] = 1
        return x, y, h_result

    def call_heuristic(self):
        if self.player_turn == 'X':
            if self.e1 == 1:
                result = self.heuristic_e1()
            else:
                result = self.heuristic_e2()
        else:
            if self.e2 == 1:
                result = self.heuristic_e1()
            else:
                result = self.heuristic_e2()

        return result

    # count num X and num O (#X-#O)
    def heuristic_e1(self):
        num_X = 0
        num_O = 0
        for column in self.current_state:
            num_X += column.count('X')
            num_O += column.count('O')
        return num_X - num_O

    # count how many X we have in column, rows and diagonals, same for Os
    def heuristic_e2(self):
        mat = [[0, 1, 2, 3, 9],
               [4, 5, 6, 7, 0],
               [8, 9, 10, 11, 18],
               [1, 2, 3, 7, 0],
               [4, 8, 5, 7, 10]]

        diagonals = []
        for j in range(self.n - self.s + 1):
            diagonal = [self.current_state[i][i + j] for i in range(self.n) if
                        0 <= i + j < self.n and 0 <= i < self.n]
            if len(diagonal) >= self.s:
                diagonals.append(diagonal)
            diagonal = [self.current_state[i][-i - j - 1] for i in range(self.n) if
                        0 <= i + j < self.n and 0 <= i < self.n]
            if len(diagonal) >= self.s:
                diagonals.append(diagonal)
        for start in range(1, self.n):
            j = 0
            diagonal = [self.current_state[start + i][i + j] for i in range(self.n) if
                        0 <= i + j < self.n and 0 <= start + i < self.n]
            if len(diagonal) >= self.s:
                diagonals.append(diagonal)
            diagonal = [self.current_state[start + i][-i - j - 1] for i in range(self.n) if
                        0 <= i + j < self.n and 0 <= start + i < self.n]
            if len(diagonal) >= self.s:
                diagonals.append(diagonal)
            j = self.n - 1
            diagonal = [self.current_state[start + i][i + j] for i in range(self.n) if
                        0 <= i + j < self.n and 0 <= start + i < self.n]
            if len(diagonal) >= self.s:
                diagonals.append(diagonal)
            diagonal = [self.current_state[start + i][-i - j - 1] for i in range(self.n) if
                        0 <= i + j < self.n and 0 <= start + i < self.n]
            if len(diagonal) >= self.s:
                diagonals.append(diagonal)

            # Horizontal win
            horizontals = []
            for i in range(self.n):
                row = []
                for column in self.current_state:
                    row.append(column[i])
                horizontals.append(row)

            all = diagonal + horizontals + self.current_state

            total = 0
            for list in all:
                current = list[0]
                current_score = 1
                for i in range(1, len(list)):
                    if list[i] != '.' and list[i] != '-':
                        if current == '':
                            current = list[i]
                        if current == list[i]:
                            current_score *= 10
                        elif current != list[i] and current == 'X':
                            if current_score != 1:
                                total += current_score
                            current_score = 10
                            current = 'O'
                        elif current != list[i] and current == 'O':
                            if current_score != 1:
                                total -= current_score
                            current_score = 10
                            current = 'X'
                    else:
                        if current == 'X':
                            if current_score != 1:
                                total += current_score
                        elif current == 'O':
                            if current_score != 1:
                                total -= current_score
                        current_score = 1
                        current = ''
            return total

    def play(self):
        if self.a1:
            algo1 = self.ALPHABETA
        else:
            algo1 = self.MINIMAX

        if self.a2:
            algo2 = self.ALPHABETA
        else:
            algo2 = self.MINIMAX

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
            self.write_board()
            if self.check_end():
                self.f.close()
                return

            self.evaluations = {}
            start = time.time()
            if algo1 == self.MINIMAX and self.player_turn == 'X':
                (x, y, h_result) = self.minimax(max=False, start=start)
            elif self.player_turn == 'X':  # algo == self.ALPHABETA
                (x, y, h_result) = self.alphabeta(max=False, start=start)
            if algo2 == self.MINIMAX and self.player_turn == 'O':
                (x, y, h_result) = self.minimax(max=True, start=start)
            elif self.player_turn == 'O':
                (x, y, h_result) = self.alphabeta(max=True, start=start)
            end = time.time()

            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                    print(F'Heuristic result: {h_result}')
                (x, y) = self.input_move()

            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
                print(F'Heuristic result: {h_result}')

                self.f.write(F"\nPlayer {self.player_turn} under AI control plays: x = {x}, y = {y}\n")

                self.f.write(F"\ni. Heuristic evaluation time: {round(end - start, 7)}s")

                values = self.evaluations.values()
                total = sum(values)
                self.f.write(F"\nii. Heuristic evaluations: {total}")
                self.f.write(F"\niii. Evaluations by depth: {self.evaluations}")
                if total != 0:
                    total_sum = sum(k*v for k, v in self.evaluations.items())/total
                else:
                    total_sum = 0
                self.f.write(F"\niv. Average evaluation depth: {total_sum}")
                self.f.write(F"\nv. Average recursion depth:")

            self.current_state[x][y] = self.player_turn
            self.switch_player()

    def get_parameters(self):
        self.n = int(input('Enter size of board (n): '))
        while self.n < 3 or self.n > 10:
            self.n = int(input('Please enter a number between 3 and 10 for n: '))

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

        mini_or_alpha = int(input('Enter 1 to use minimax or 2 to use alphabeta for player 1: '))
        while mini_or_alpha != 1 and mini_or_alpha != 2:
            mini_or_alpha = int(input('Enter 1 to use minimax or 2 to use alphabeta for player 1: '))
        if mini_or_alpha == 1:
            self.a1 = False
        else:
            self.a1 = True

        mini_or_alpha = int(input('Enter 1 to use minimax or 2 to use alphabeta for player 2: '))
        while mini_or_alpha != 1 and mini_or_alpha != 2:
            mini_or_alpha = int(input('Enter 1 to use minimax or 2 to use alphabeta for player 2: '))
        if mini_or_alpha == 1:
            self.a2 = False
        else:
            self.a2 = True

        e1_or_e2 = int(input('Enter 1 to use heuristic 1 or 2 to use heuristic 2 for player 1: '))
        while e1_or_e2 != 1 and e1_or_e2 != 2:
            e1_or_e2 = int(input('Enter 1 to use heuristic 1 or 2 to use heuristic 2 for player 1: '))
        self.e1 = e1_or_e2

        e1_or_e2 = int(input('Enter 1 to use heuristic 1 or 2 to use heuristic 2 for player 2: '))
        while e1_or_e2 != 1 and e1_or_e2 != 2:
            e1_or_e2 = int(input('Enter 1 to use heuristic 1 or 2 to use heuristic 2 for player 2: '))
        self.e2 = e1_or_e2

        self.player1_type = input('Enter H or AI for player 1: ')
        self.player2_type = input('Enter H or AI for player 2: ')

        self.f = open(F"gameTrace-{self.n}-{self.b}-{self.s}-{self.t}", "a")
        self.f.write(F"n={self.n} b={self.b} s={self.s} t={self.t}")
        if self.b_positions:
            self.f.write(F"\nblocks: {self.b_positions}")
        self.f.write(F"\n\nPlayer 1: {self.player1_type} d={self.d1} a={self.a1} e{self.e1}")
        self.f.write(F"\nPlayer 2: {self.player2_type} d={self.d2} a={self.a2} e{self.e2}")


def main():
    g = Game(recommend=True)
    g.play()


if __name__ == "__main__":
    main()
