import pygame as pg


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
            x = INDENT + cell_size * i + cell_size // 3
            y = INDENT + cell_size * j + cell_size // 4
            draw_text(scr, str(table[i][j]), 36, WHITE, BLACK, (x, y))


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

# =============================== Working Area =============================================

screen, clock = init('СУДОКУ')
sudoku = create_table()  # создаем таблицу судоку

while True:
    screen.fill(WHITE)
    for e in pg.event.get():
        exit(e)
    draw_table(sudoku, screen)
    pg.display.update()
    clock.tick(FPS)
