import pygame
import player
import game_objects
from constants import *
from level import *
class Game:
    def __init__(self):
        # инициализируем библиотеку pygame
        pygame.init()
        self.levels = Level()
        # создаем графическое окно
        WIN_WIDTH = self.levels.map_width
        WIN_HEIGHT = self.levels.map_height
        self.screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        self.background_img = pygame.image.load("background.png").convert()
        pygame.display.set_caption("Platformer")
        self.level_num = 0
        self.clock = pygame.time.Clock()
        # Задаем текущие состоятния игры ("START", "GAME", "PAUSE" или "FINISH")
        self.state = "GAME"

    def create_level(self):
        # создаем группу для всех спрайтов в игре
        self.all_sprite_list = pygame.sprite.Group()

        # Создаем спрайт игрока
        self.player = player.Player()
        self.all_sprite_list.add(self.player)

        # связываем координаты с определениями объектов для текущего уровня
        self.player.rect.x, self.player.rect.y = self.levels.load_level(self.level_num)

        # создаем группу спрайтов - препятствий (платформ)
        self.platform_list = pygame.sprite.Group()

        # Создаем стены и платформы
        for coord in self.levels.platform_coords:
            platform = game_objects.Platform(coord[0], coord[1])
            self.platform_list.add(platform)
            self.all_sprite_list.add(platform)
        self.artifact_list = pygame.sprite.Group()

        # Создаем артефакты
        # Создаем артефакты (монеты) в игре
        for coord in self.levels.artifact_coords:
            artifact = game_objects.Artifact(coord[0], coord[1])
            self.artifact_list.add(artifact)
            self.all_sprite_list.add(artifact)

        # Задаем группу спрайтов - препятствий для игрока
        self.player.platforms = self.platform_list
        self.player.artifacts = self.artifact_list

    def handle_scene(self, event):
        # обрабатываем сцену Идет Игра
        if self.state == "GAME":
            # обрабатываем нажатие клавиш - стрелок
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.go_right()
                elif event.key == pygame.K_UP:
                    self.player.jump()
                # переключение уровней на клавишу L
                elif event.key == pygame.K_l:
                    self.level_num = (self.level_num + 1) % len(self.levels.maps)
                    self.create_level()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()

        # обрабатываем сцену Игра Закончена
        elif self.state == "FINISH":
            pass
        # Обрабатываем сцену Стартовый экран
        elif self.state == "START" :
            pass

    def draw_scene(self):
        # Выполняем заливку экрана
        self.screen.blit(self.background_img, (0, 0))
        # Обрабатываем сцену Идет Игра
        if self.state == "GAME":
            self.all_sprite_list.draw(self.screen)
        # Обрабатываем сцену Стартовый экран
        elif self.state == "START": pass
        # Обрабатываем сцену Пауза
        elif self.state == "PAUSE": pass
        # Обрабатываем сцену Игра Окончена
        elif self.state == "FINISH": pass
    
    def run(self):
        done = False
        # создаем текущий уровень
        self.create_level()
        while not done:
            for event in pygame.event.get():
                # Обрабатываем закрытие окна
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.level_num += 1
                        self.level_num %= 3 
                        self.create_level()

                # Обрабатываем события для разных состояний игры:
                self.handle_scene(event)
            # Если идет игра, обновляем положение всех спрайтов в игре:
            if self.state == "GAME":
                self.all_sprite_list.update()
            # Прорисовываем экран в зависимости от состояния игры 
            self.draw_scene()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

game = Game()
game.run()