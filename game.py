import pygame
from constants import RED, YELLOW, ROWS, COLS, PADDING_X, PADDING_Y, COL_PAD

pygame.font.init()


class Game:
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height
        self.color = (0, 0, 255)
        self.x = 0
        self.y = 100
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.wins = [0, 0]
        self.ties = 0
        self.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]]

    def won(self, player):
        self.wins[player] += 1

    def tied(self):
        self.ties += 1

    def draw(self, win):
        font = pygame.font.SysFont("Comic Sans MS", 40)
        ties = str(self.ties)
        text = font.render("Ties: " + ties, True, (255, 0, 0))
        win.blit(text, (20, 0))

        fnt = pygame.font.SysFont("Comic Sans MS", 20)
        for num in range(1, COLS+1):
            text = fnt.render(str(num), True, (255, 0, 0))
            win.blit(text, (COL_PAD + ((num-1)*100), 65))

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    pygame.draw.circle(win, (255, 255, 255), (PADDING_X + (col * 100), PADDING_Y + (row * 100)), 27)
                elif self.board[row][col] == RED:
                    pygame.draw.circle(win, RED, (PADDING_X + (col * 100), PADDING_Y + (row * 100)), 27)
                else:
                    pygame.draw.circle(win, YELLOW, (PADDING_X + (col * 100), PADDING_Y + (row * 100)), 27)

    def findEmpty(self, col):
        column = [row[col] for row in self.board]
        length = len(column) - 1

        while length >= 0:
            print(length)
            if column[length] == 0:
                return length
            else:
                length -= 1

        return -1

    def update_board(self, player, move):
        col = move
        row = self.findEmpty(col)

        if row >= 0:
            if player == 0:
                self.board[row][col] = RED
            else:
                self.board[row][col] = YELLOW

            return True
        else:
            return None

    def play(self, player, move):
        valid = self.update_board(player, move)

        if valid:
            if player == 0:
                self.p1Went = True
            else:
                self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def check_verticals(self, color):
        for col in range(COLS):
            counter = 0
            for row in range(ROWS):
                if self.board[row][col] == color:
                    counter += 1
                    if counter == 4:
                        return True
                else:
                    counter = 0
        return False

    def check_horizontals(self, color):
        for row in range(ROWS):
            counter = 0
            for col in range(COLS):
                if self.board[row][col] == color:
                    counter += 1
                    if counter == 4:
                        return True
                else:
                    counter = 0
        return False

    def check_diagonal_right(self, color):
        for row in range(3, 6):
            counter = 0
            col = 0
            while row >= 0:
                if self.board[row][col] == color:
                    counter += 1
                    if counter == 4:
                        return True
                else:
                    counter = 0

                row -= 1
                col += 1

        for col in range(1, 4):
            counter = 0
            row = 5
            while col < 7:
                if self.board[row][col] == color:
                    counter += 1
                    if counter == 4:
                        return True
                else:
                    counter = 0

                row -= 1
                col += 1

        return False

    def check_diagonal_left(self, color):
        for row in range(3, 6):
            counter = 0
            col = 6
            while row >= 0:
                if self.board[row][col] == color:
                    counter += 1
                    if counter == 4:
                        return True
                else:
                    counter = 0

                row -= 1
                col -= 1

        for col in range(3, 6):
            counter = 0
            row = 5
            while col >= 0:
                if self.board[row][col] == color:
                    counter += 1
                    if counter == 4:
                        return True
                else:
                    counter = 0

                row -= 1
                col -= 1

        return False

    def winner(self):
        if self.check_verticals(RED) or self.check_horizontals(RED) or self.check_diagonal_left(RED) or \
                self.check_diagonal_right(RED):
            return 0
        elif self.check_verticals(YELLOW) or self.check_horizontals(YELLOW) or self.check_diagonal_left(YELLOW) or \
                self.check_diagonal_right(YELLOW):
            return 1
        elif self.is_finished():
            return -1
        else:
            return -2

    def is_finished(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    return False
        return True

    def reset_went(self):
        self.p1Went = False
        self.p2Went = False

    def reset_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != 0:
                    self.board[row][col] = 0
