import pygame
from constants import *
from level import *
from spritesheet_functions import SpriteSheet
 
class Player(pygame.sprite.Sprite):
    # Этот класс описывает управление и поведение спрайта игрока
    # Конструктор класса
    def __init__(self, x=0, y=0):
        super().__init__()
        
        # Задаем скорость игрока по x и по y
        self.change_x = 0
        self.change_y = 0
        self.platforms = pygame.sprite.Group()
        # Добавляем поле artifacts:
        self.artifacts = pygame.sprite.Group()
        self.score = 0

        self.walking_frames_l = []
        self.walking_frames_r = []

        self.direction = "R"

        sprite_sheet = SpriteSheet("p1_walk.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_r.append(image)
 
        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    # Расчет гравитации
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            # Моделируем ускорение свободного падения:
            self.change_y += .35

        # Проверка: персонаж на земле или нет
        if self.rect.y >= WIN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = WIN_HEIGHT - self.rect.height
    
    def update(self):
        # учитываем эффект гравитации:
        self.calc_grav()
        # Пересчитываем положение спрайта игрока на экране
        # Смещение влево - вправо
        self.rect.x += self.change_x
        if self.direction == "R":
            frame = self.rect.x % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = self.rect.x % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        # Проверяем столкновение с препятствием
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            # Если персонаж двигался вправо, остановим его слева от препятствия
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Наоборот, если движение было влево остановим его справа от препятствия
                self.rect.left = block.rect.right

        # Движение вверх-вниз
        self.rect.y += self.change_y

        # Проверяем столкновение с препятствием
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            # При движении вниз, персонаж упал на препятствие - он должен встать на него сверху
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # В прыжке персонаж врезался в препятствия - движение вверх должно прекратиться.
            self.change_y = 0

        # Проверяем столкновение с артефактом
        artifact_hit_list = pygame.sprite.spritecollide(self, self.artifacts, False)
        for artifact in artifact_hit_list:
            self.score += 1
            artifact.kill()

    def jump(self):
        # двигаемся вниз на 2 пикселя, чтобы убедиться, что под игроком есть платформа
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 2

        # если платформа есть, то можно прыгнуть, оттолкнувшись от нее
        if len(platform_hit_list) > 0 or self.rect.bottom >= WIN_HEIGHT:
            self.change_y = -10

    # Управление игроком:
    def go_left(self):
        # Нажатие кнопки влево. 
        self.change_x = -6
        self.direction = "L"

    def go_right(self):
        # Нажатие кнопки вправо. 
        self.change_x = 6
        self.direction = "R"

    def stop(self):
        # Отпустили кнопку, прекратили движение по горизонтали 
        self.change_x = 0