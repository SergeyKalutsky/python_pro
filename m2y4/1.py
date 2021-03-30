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


FPS = 30
WIN_WIDTH = 500 # ширина графического окна
WIN_HEIGHT = 500 # высота графического окна
INDENT = 20 # поля вокруг таблицы
# наша палитра :
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255,0)

# =============================== Working Area =============================================

screen, clock = init('СУДОКУ')

while True:
    for e in pg.event.get():
        exit(e)
    clock.tick(FPS)
