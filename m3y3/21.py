""" --------------------------------------------------------
Проект "Гонки". Загружено фоновое изображение
-------------------------------------------------------- """
import pygame as pg
from random import randrange

WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 30
# цвета    R    G    B
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (255, 0,   0)
GREEN = (0,   255, 0)
BLUE = (0,   0,   255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)


class Block(pg.sprite.Sprite):
    def __init__(self, color, size=30, speed=5, pos=None):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Create an image of the block, and fill it with a color.
        self.image = pg.Surface([size, size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = randrange(WIN_WIDTH) if pos is None else pos[0]
        self.rect.y = randrange(WIN_HEIGHT) if pos is None else pos[1]
        self.speed = speed

    def update(self):
        # Подвинуть блок "навстречу" автомобилю
        self.rect.y += self.speed
        if self.rect.y > WIN_WIDTH:
            self.rect.y = 0
            self.rect.x = randrange(WIN_WIDTH)


def init(caption):
    pg.init()
    screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pg.display.set_caption(caption)
    clock = pg.time.Clock()
    return screen, clock


def quit(e):
    if e.type == pg.QUIT:
        pg.quit()


def gen_enemies(n, block_list, all_sprites_list):
    for _ in range(n):
        block = Block(BLACK)
        block_list.add(block)
        all_sprites_list.add(block)
    return block_list, all_sprites_list


def draw_text(screen, text, font_size, text_color, pos):
    basic_font = pg.font.SysFont('Arial', font_size)
    text = basic_font.render(text, True, text_color)
    screen.blit(text, pos)



screen, clock = init('ГОНКИ')

# Создаем группы спрайтов:
block_list = pg.sprite.Group()
all_sprites_list = pg.sprite.Group()
block_list, all_sprites_list = gen_enemies(10, block_list, all_sprites_list)

EXTNS = ['png', 'gif', 'jpg', 'jpeg', 'bmp']
name = 'wallpaper'
for ext in EXTNS:
    path = name + '.' + ext
    try:
        start_image = pg.image.load(path).convert()
        break
    except:
        pass

# Создаем спрайт игрока
x = WIN_WIDTH // 2
y = WIN_HEIGHT - 50
player = Block(RED, 40, 0, (x, y))
all_sprites_list.add(player)

run = True
while True:
    for i in pg.event.get():
        quit(i)

    if run:
        pos = pg.mouse.get_pos()
        player.rect.x = pos[0] - 20
        block_list.update()

    screen.fill(GRAY)
    screen.blit(start_image, [0, 0])
    all_sprites_list.draw(screen)

    if pg.sprite.spritecollideany(player, block_list):
        run = False
        text_pos = (WIN_WIDTH // 3, WIN_HEIGHT // 3)
        draw_text(screen, 'YOU CRASHED!', 36, RED, text_pos)

    pg.display.update()
    clock.tick(FPS)
