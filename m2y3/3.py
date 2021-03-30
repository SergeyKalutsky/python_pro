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

circle1, circle2, sqr = {}, {}, {}

circle1['x'] = 150
circle1['y'] = 150
circle1['r'] = 100

circle2['x'] = circle1['x'] + circle1['r']
circle2['y'] = circle1['y']
circle2['r'] = circle1['r']

sqr['x'] = circle1['x']
sqr['y'] = circle1['y'] - circle1['r']
sqr['h'] = circle1['r']
sqr['w'] = circle1['r']*2



screen, clock = init('Привет pygame!')

run = True
while run:
    screen.fill(WHITE)
    for e in pygame.event.get():
        quit(e, run)
        
    draw_circle(screen, GREEN, circle1)
    draw_circle(screen, GREEN, circle2)
    draw_rect(screen, RED, sqr)
    pygame.display.update()
    clock.tick(FPS)