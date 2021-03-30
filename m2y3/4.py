import pygame


def init(caption):
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()
    return screen, clock


def quit(e, run):
    if e.type == pygame.QUIT:
        run = False
        pygame.quit()    


def draw_circle(screen, color, circle):
    pygame.draw.circle(screen, color, (circle['x'], circle['y']), circle['r'])


def draw_rect(screen, color, sqr):
    square = pygame.Rect(sqr['x'], sqr['y'], sqr['h'], sqr['w'])
    pygame.draw.rect(screen, color, square)


def draw_ellipse(screen, color, sqr):
    ellipse_rect = pygame.Rect(sqr['x'], sqr['y'], sqr['h'], sqr['w'])
    pygame.draw.ellipse(screen, color, ellipse_rect)

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


screen, clock = init('Привет pygame!')

run = True
while run:
    screen.fill(WHITE)
    for e in pygame.event.get():
        quit(e, run)
        
    draw_circle(screen, RED, circle)
    draw_rect(screen, YELLOW, sqr)
    draw_ellipse(screen, GREEN, sqr2)
    pygame.display.update()
    clock.tick(FPS)