""" --------------------------------------------------------
Проект "Гонки". Загружено фоновое изображение
-------------------------------------------------------- """
import pygame as pg
from random import randrange, randint

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


class Car(pg.sprite.Sprite):
    def __init__(self, x, y, img='Car.png'):
        super().__init__()
        self.image = pg.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Block(pg.sprite.Sprite):
    image_list = ['Ambulance.png',
                  'Black_car.png',
                  'Mini_truck.png',
                  'Mini_van.png',
                  'taxi.png',
                  'Red_car.png']

    def __init__(self, color=None, size=30, speed=5, pos=None):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Create an image of the block, and fill it with a color.
        img = self.image_list[randint(0, 5)]
        self.image = pg.image.load(img).convert_alpha()
        self.image = pg.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = randrange(WIN_WIDTH)
        self.rect.y = randrange(-200, WIN_HEIGHT - 200)
        self.speed = speed

    def update(self):
        # Подвинуть блок "навстречу" автомобилю
        self.rect.y += self.speed
        if self.rect.y > WIN_HEIGHT:
            self.__init__(self.speed)
            self.rect.y = -50


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
        block = Block(speed=5)
        block_list.add(block)
        all_sprites_list.add(block)
    return block_list, all_sprites_list


def draw_text(screen, text, font_size, text_color, pos):
    basic_font = pg.font.SysFont('Arial', font_size)
    text = basic_font.render(text, True, text_color)
    screen.blit(text, pos)


def change_state(e, current_state):
    if e.type == pg.KEYDOWN:
        if e.key == pg.K_SPACE:
            if current_state == 0:  # начать игру
                current_state = 1
            elif current_state == 1:  # идет игра, нажали PAUSE
                current_state = 2
            elif current_state == 2:  # сняли с паузы
                current_state = 1
    return current_state


screen, clock = init('ГОНКИ')

# Создаем группы спрайтов:
block_list = pg.sprite.Group()
all_sprites_list = pg.sprite.Group()
block_list, all_sprites_list = gen_enemies(10, block_list, all_sprites_list)

start_image = pg.image.load("wallpaper.png").convert()

# Создаем спрайт игрока
x = WIN_WIDTH // 2
y = WIN_HEIGHT - 50
player = Car(WIN_WIDTH // 2, WIN_HEIGHT - 100)
all_sprites_list.add(player)

text_pos = (WIN_WIDTH // 3.5, WIN_HEIGHT // 3)

current_state = 0
while True:
    screen.fill(GRAY)
    for i in pg.event.get():
        quit(i)
        current_state = change_state(i, current_state)

    if current_state == 1:
        pos = pg.mouse.get_pos()
        player.rect.x = pos[0] - 20
        block_list.update()
        all_sprites_list.draw(screen)

    if pg.sprite.spritecollideany(player, block_list):
        current_state = 3

    if current_state == 0:
        screen.blit(start_image, (0, 0))
        draw_text(screen, 'PRESS SPACE TO START', 36, RED, text_pos)

    if current_state == 2:
        all_sprites_list.draw(screen)
        draw_text(screen, 'PAUSE', 36, RED, text_pos)

    if current_state == 3:
        # если случилось столкновение, выводим надпись:
        draw_text(screen, 'YOU CRASHED!', 36, RED, text_pos)

    pg.display.update()
    clock.tick(FPS)
