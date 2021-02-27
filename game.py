import pygame
import random
import os
import sys

SIZE = WIDTH, HEIGTH = 604, 705
CELL = 30
POS_X = 15
POS_Y = 15
SNAKE = [(POS_Y, POS_X)]
PAUSE = False
LEVEL = 1
SCORE = 0
ERROR_snake = False

# Открываем текстовый файл с рекордом предыдущих игр
with open('date/scores.txt', 'r') as f:
    lines = f.readlines()
    RECORD = lines[0].strip()


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * self.width for _ in range(self.height)]
        self.board_cord = [[0] * width for _ in range(height)]
        self.left = 1
        self.top = 103
        self.cell_size = 20
        self.apple_y = random.randint(0, 15)
        self.apple_x = random.randint(0, 15)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):  # Рисование
        x = self.left
        y = self.top
        for i in range(self.height):
            for j in range(self.width):
                self.board_cord[i][j] = (x, y, x + self.cell_size, y + self.cell_size)
                if self.board[i][j] == 1:  # прорисовка змейки
                    pygame.draw.rect(screen, ('green'), (x + 1, y + 1, self.cell_size, self.cell_size), 0)
                    pygame.draw.rect(screen, ('green'), (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1), 1)
                elif self.board[i][j] == 2:  # прорисовка яблока
                    pygame.draw.rect(screen, ('red'), (x + 1, y + 1, self.cell_size, self.cell_size), 0)
                    pygame.draw.rect(screen, ('red'), (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1), 1)
                else:  # прорисовка поля
                    pygame.draw.rect(screen, ('#808080'), (x, y, self.cell_size + 1, self.cell_size + 1), 1)
                x += self.cell_size
            x = self.left
            y += self.cell_size

    def traffic_snake(self):
        global SNAKE, POS_Y, POS_X, UP_DOWN_SNAKE, RIGHT_LEFT_SNAKE, SCORE, PAUSE, ERROR_snake

        cx, cy = POS_X, POS_Y

        POS_X += RIGHT_LEFT_SNAKE
        POS_Y += UP_DOWN_SNAKE
        if (POS_Y > 29 or POS_Y < 0) or (POS_X > 29 or POS_X < 0):
            ERROR_snake = True
            POS_X, POS_Y = cx, cy
        elif not PAUSE:
            if self.board[POS_Y][POS_X] == 1:
                ERROR_snake = True
                POS_X, POS_Y = cx, cy

        if not PAUSE and not ERROR_snake:
            SNAKE.append((POS_Y, POS_X))
            del_cell = SNAKE.pop(0)
            self.board[del_cell[0]][del_cell[1]] = 0


        for pos_snake in SNAKE:
            self.board[pos_snake[0]][pos_snake[1]] = 1

        # Если змея съедает яблоко
        if POS_X == self.apple_x and POS_Y == self.apple_y:
            self.addition_snake()

        # Вызов метода добавления ябока на поле
        self.append_apple()

    # Метод добавления ябока на поле
    def append_apple(self):
        if not any(k == 2 for v3 in self.board for k in v3):  # случайным образом появляется яблоко
            while self.board[self.apple_y][self.apple_x] == 1:
                self.apple_y = random.randint(0, 15)
                self.apple_x = random.randint(0, 15)
            self.board[self.apple_y][self.apple_x] = 2

    # Метод добавления клетки змейке при съедании яблока
    def addition_snake(self):
        global POS_Y, POS_X, SCORE
        SNAKE.insert(0, (POS_Y, POS_X))
        SCORE += 1
        self.update_record()

    def update_record(self):
        global SCORE
        # Если игрок достиг нового рекорда обновляем старый - открываем текстовый файл с рекордом
        with open('date/scores.txt', 'r') as f:
            lines = f.readlines()
            old_record = lines[0].strip()
        with open('date/scores.txt', 'w') as f:
            if SCORE > int(old_record):
                f.write(str(SCORE))
            else:
                f.write(str(RECORD))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра "Змейка"')
    screen = pygame.display.set_mode(SIZE)
    board = Board(CELL, CELL)


    # Загружаем музыку
    def fullname_for_music_file(name, colorkey=None):
        fullname = os.path.join('date', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с аудио '{fullname}' не найден")
            sys.exit()
        return fullname


    pygame.mixer.music.load(fullname_for_music_file('main_music.mp3'))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1, 0.0)

    UP_DOWN_SNAKE, RIGHT_LEFT_SNAKE = 0, 1  # начальное напраление движения змейки
    SPEED_SNAKE = 0.05  # скорость движения змейки

    count = 1
    fps = 60
    running = True
    clock = pygame.time.Clock()
    while running:
        # прием и обработка сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and not PAUSE:
                    if RIGHT_LEFT_SNAKE == 0:
                        RIGHT_LEFT_SNAKE, UP_DOWN_SNAKE = 1, 0
                if event.key == pygame.K_LEFT and not PAUSE:
                    if RIGHT_LEFT_SNAKE == 0:
                        RIGHT_LEFT_SNAKE, UP_DOWN_SNAKE = -1, 0
                if event.key == pygame.K_UP and not PAUSE:
                    if UP_DOWN_SNAKE == 0:
                        UP_DOWN_SNAKE, RIGHT_LEFT_SNAKE = -1, 0
                if event.key == pygame.K_DOWN and not PAUSE:
                    if UP_DOWN_SNAKE == 0:
                        UP_DOWN_SNAKE, RIGHT_LEFT_SNAKE = 1, 0
                if event.key == pygame.K_SPACE:
                    if SCORE % 10 == 0 and SCORE:
                        SCORE += 1
                        SPEED_SNAKE += 0.01
                        LEVEL += 1
                    else:
                        if PAUSE:
                            PAUSE = False
                            UP_DOWN_SNAKE, RIGHT_LEFT_SNAKE = save_UP_DOWN_SNAKE, save_RIGHT_LEFT_SNAKE
                        else:
                            save_UP_DOWN_SNAKE, save_RIGHT_LEFT_SNAKE = UP_DOWN_SNAKE, RIGHT_LEFT_SNAKE
                            UP_DOWN_SNAKE, RIGHT_LEFT_SNAKE = 0, 0
                            PAUSE = True

        screen.fill((240, 240, 240))
        board.render()

        count += SPEED_SNAKE
        if round(count) > 0:
            board.traffic_snake()
            count = 0

        game_process = pygame.font.SysFont('Arial', 25, True, False)
        text_level = game_process.render("Уровень: " + str(LEVEL), True, (0, 0, 0))
        screen.blit(text_level, [1, 1])
        text_score = game_process.render("Очки: " + str(SCORE), True, (0, 0, 0))
        screen.blit(text_score, [1, 30])
        text_record = game_process.render("Рекорд: " + str(RECORD), True, (0, 0, 0))
        screen.blit(text_record, [1, 60])

        # Надпись 'Пауза'
        if PAUSE:
            game_pause = pygame.font.SysFont('Arial', 50, True, False)
            text_pause = game_pause.render('Пауза!', True, ('red'))
            screen.blit(text_pause, [150, 20])

        # переход на новый уровень
        if SCORE % 10 == 0 and SCORE:
            POS_X = 15
            POS_Y = 15
            SNAKE = [(POS_Y, POS_X)]
            board.board = [[0] * board.width for _ in range(board.height)]
            UP_DOWN_SNAKE, RIGHT_LEFT_SNAKE = 0, 1
            game_lavel = pygame.font.SysFont('Arial', 20, True, False)
            text_1 = game_lavel.render('Продолжить? Нажмите ПРОБЕЛ!', True, ('red'))
            screen.blit(text_1, [150, 20])

        if ERROR_snake:
            game_over = pygame.font.SysFont('Arial', 50, True, False)
            text_over = game_over.render('Конец игры!', True, ('red'))
            screen.blit(text_over, [150, 20])

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
