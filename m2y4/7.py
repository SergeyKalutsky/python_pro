import pygame as pg
import sys


def init(caption):
    pg.init()
    screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pg.display.set_caption(caption)
    clock = pg.time.Clock()
    return screen, clock


def exit(e):
    if e.type == pg.QUIT:
        pg.quit()


def draw_circle(screen, color, circle):
    pg.draw.circle(screen, color, (circle['x'], circle['y']), circle['r'])


def draw_rect(screen, color, sqr):
    square = pg.Rect(sqr['x'], sqr['y'], sqr['h'], sqr['w'])
    pg.draw.rect(screen, color, square)


def draw_ellipse(screen, color, sqr):
    ellipse_rect = pg.Rect(sqr['x'], sqr['y'], sqr['h'], sqr['w'])
    pg.draw.ellipse(screen, color, ellipse_rect)


def draw_text(screen, text, font_size, background_color, text_color, pos):
    basic_font = pg.font.SysFont(None, font_size)
    text = basic_font.render(text, True, text_color, background_color)
    screen.blit(text, pos)


def create_table():
    table = []
    table.append([7, 1, 4, 8, '☐', 5, '☐', 9, 3])
    table.append([8, 2, 5, 9, '☐', 6, 7, 1, '☐'])
    table.append([9, 3, '☐', '☐', '☐', 7, 8, 2, 5])
    table.append([2, 5, 8, 3, 6, 9, '☐', 4, '☐'])
    table.append(['☐', 4, 7, 2, 5, 8, 9, 3, 6])
    table.append([3, 6, 9, 4, 7, 1, 2, 5, '☐'])
    table.append([5, 8, 2, 6, 9, 3, 4, 7, 1])
    table.append([4, 7, 1, 5, '☐', '☐', 3, 6, 9])
    table.append(['☐', 9, '☐', 7, 1, 4, '☐', 8, 2])
    return table


def draw_table(table, scr, active_row=-1, active_column=-1, the_end=False):
    cell_size = (WIN_WIDTH - INDENT * 2) // 9
    for i in range(9):
        for j in range(9):
            if i == active_row and j == active_column:
                background_color = YELLOW
            else:
                background_color = WHITE
            x = INDENT + cell_size * i + cell_size // 3
            y = INDENT + cell_size * j + cell_size // 4
            draw_text(scr, str(table[i][j]), 36,
                      background_color, BLACK, (x, y))
    if the_end:
        draw_text(scr, 'ГОТОВО!', 48, GREEN, RED, (150, 200))


def get_cell(x, y):
    cell_size = (WIN_WIDTH - INDENT * 2) // 9
    for i in range(9):
        for j in range(9):
            x0 = INDENT + cell_size * i  # левая граница ячейки
            y0 = INDENT + cell_size * j  # верхняя граница ячейки
            if x0 < x < x0 + cell_size and y0 < y < y0 + cell_size:
                return (i, j)
    return (-1, -1)


def check_a_move(table, row_index, col_index, digit):
    if not ((0 <= row_index < 9) and (0 <= col_index < 9) and (1 <= digit <= 9)):
        return 'Некорретный ход'
    if table[row_index][col_index] != '☐':
        return 'Эта ячейка уже заполнена'
    digits_in_row = {digit} 
    digits_in_column = {digit}
    for i in range(9):
        if table[row_index][i] != '☐':
            if table[row_index][i] in digits_in_row:
                return 'Повтор цифры в строке'
            else:
                digits_in_row.add(table[row_index][i])
        if table[i][col_index] != '☐':
            if table[i][col_index] in digits_in_column:
                return 'Повтор цифры в столбце'
            else:
                digits_in_column.add(table[i][col_index])
    return ''


def free_cells(table):
    n = 0
    for row in table:
        n += row.count('☐')
    return n


FPS = 30
WIN_WIDTH = 500  # ширина графического окна
WIN_HEIGHT = 500  # высота графического окна
INDENT = 20  # поля вокруг таблицы
# наша палитра :
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

KEYS = {
    pg.K_0: 0,
    pg.K_1: 1,
    pg.K_2: 2,
    pg.K_3: 3,
    pg.K_4: 4,
    pg.K_5: 5,
    pg.K_6: 6,
    pg.K_7: 7,
    pg.K_8: 8,
    pg.K_9: 9
}

# =============================== Working Area =============================================

screen, clock = init('СУДОКУ')
sudoku = create_table()  # создаем таблицу судоку
hint_pos = (INDENT, 5)
act_row, act_column = -1, -1
hint = 'Кликните на пустую ячейку и введите цифру'

while True:
    screen.fill(WHITE)
    for e in pg.event.get():
        exit(e)
        if e.type == pg.MOUSEBUTTONDOWN:
            # проверяем, что нажали левую кнопку:
            if e.button == 1:
                act_row, act_column = get_cell(*e.pos)
        if e.type == pg.KEYDOWN:
            digit = KEYS[e.key] if e.key in KEYS else -1
            hint = check_a_move(sudoku, act_row, act_column, digit)
            if not hint:
                sudoku[act_row][act_column] = digit
                if free_cells(sudoku) == 0:
                    the_end = True

    draw_table(sudoku, screen, act_row, act_column)
    draw_text(screen, hint, 35, BLUE, WHITE, hint_pos)
    pg.display.update()
    clock.tick(FPS)
