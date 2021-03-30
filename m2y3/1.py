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

screen, clock = init('Привет pygame!')

run = True
while run:
   for e in pygame.event.get():
       screen.fill(WHITE)
       quit(e, run)
   clock.tick(FPS)