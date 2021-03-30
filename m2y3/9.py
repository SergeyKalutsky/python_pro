import pygame as pg 


def init(caption):
    pg.init()
    screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pg.display.set_caption(caption)
    clock = pg.time.Clock()
    return screen, clock


def quit_pg(e):
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


# наша палитра :
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255,0)

FPS = 30
WIN_WIDTH = 500 # ширина графического окна
WIN_HEIGHT = 500 # высота графического окна
# Код пишем ниже
# *************************************************************************************************

circle, sqr, sqr2 = {}, {}, {}
circle['x'] = WIN_WIDTH // 3
circle['y'] = WIN_WIDTH // 3
circle['r'] = 35

sqr['x'] = 20
sqr['y'] = 30
sqr['w'], sqr['h'] = 50, 50

sqr2['x'] = 60
sqr2['y'] = 60
sqr2['w'], sqr2['h'] = 100, 200


screen, clock = init('Привет PYGAME!')
text_pos = (100, 10)
run = True
while run:
    screen.fill(WHITE)
    for e in pg.event.get():
        quit_pg(e)
        if e.type == pg.MOUSEMOTION:
            circle['x'], circle['y'] = e.pos
        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                text_pos = e.pos
        
    draw_circle(screen, RED, circle)
    draw_rect(screen, YELLOW, sqr)
    draw_ellipse(screen, GREEN, sqr2)
    draw_text(screen, 'Hi there', 40, RED, BLACK, text_pos)
    pg.display.update()
    clock.tick(FPS)