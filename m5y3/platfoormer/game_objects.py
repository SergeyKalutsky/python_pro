import pygame
from spritesheet_functions import SpriteSheet
from constants import *

class Platform(pygame.sprite.Sprite):
    """ Платформы на которые может запрыгивать игрок """
    def __init__(self, x, y):
        super().__init__()
        sprite_sheet = SpriteSheet("world_spritesheet.png")
        # Вырезаем изображение из спрайтшита
        self.image = sprite_sheet.get_image(0, 0, 40, 40)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Artifact(pygame.sprite.Sprite):
    """ Артефакты в игре """
    def __init__(self, x, y):
        super().__init__()
        sprite_sheet = SpriteSheet("world_spritesheet.png")
        # Вырезаем изображение из спрайтшита
        self.image = sprite_sheet.get_image(42, 0, 40, 40)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x