'''
Модуль 4
Результат работы на уроке 3
Проект платформер. Добавлено главное меню.
'''
import pygame
import game_object
from constants import *
from game_menu import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        pygame.display.set_caption('Test')
        self.background_img = pygame.image.load("background.png").convert()
        self.all_sprite_list = pygame.sprite.Group()
        # Создаем платформы
        self.platform_list = pygame.sprite.Group()
        self.create_walls()
        # Создаем артефакты
        self.artifact_list = pygame.sprite.Group()
        self.create_artifacts()
        # Создаем спрайт игрока
        self.player = game_object.Player(0, 0)
        self.player.platforms = self.platform_list
        self.player.artifacts = self.artifact_list
        self.all_sprite_list.add(self.player)
        self.enemy_list = pygame.sprite.Group()
        self.create_enemies()
        # Создаем меню
        self.top_panel = TopPanel(20, 10)
        self.main_menu = MainMenu(300, 200)

        self.clock = pygame.time.Clock()

        # states: 'START', 'GAME', 'PAUSE', 'FINISH', 'GAME_OVER'
        self.state = 'START'
        self.time = 0
    
    def create_enemies(self):
        # Создаем противников в игре
        enemies_coords = [
            [150, 350, 400],
            [500, 550, 750],
            [1250,550, 1400]
        ]
        for coord in enemies_coords:
            enemy = game_object.Enemy(coord[0], coord[1])
            enemy.stop = coord[2]
            self.enemy_list.add(enemy)
            self.all_sprite_list.add(enemy)

    def create_walls(self):
        # Создаем стены и платформы
        platform_coords = [
            [0, 600],
            [155, 345],
            [320, 350],
            [550, 245],
            [735, 125],
            [0, 300],
            [0, 590],
        ]
        for coord in platform_coords:
            platform = game_object.Platform(coord[0], coord[1])
            self.platform_list.add(platform)
            self.all_sprite_list.add(platform)

    def create_artifacts(self):
        # Создаем артефакты (монеты) в игре
        artifact_coords = [
            [170, 305],
            [320, 310],
            [370, 310],
            [420, 310],
            [565, 205],
            [745, 85]
        ]
        for coord in artifact_coords:
            artifact = game_object.Artifact(coord[0], coord[1])
            self.artifact_list.add(artifact)
            self.all_sprite_list.add(artifact)



    def handle_scene(self, event):
        if self.state == 'GAME':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.go_right()
                elif event.key == pygame.K_UP:
                    self.player.jump()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()
                elif event.key == pygame.K_ESCAPE:
                    self.state = 'PAUSE'

        # Если игра не идет, значит на экране главное меню
        # Обрабатываем события главного меню:
        else:
            # Получаем кнопку, на которую нажали в главном меню:
            active_button = self.main_menu.handle_mouse_event(event.type)
            if active_button:
                # После того, как на кнопку нажали, возвращаем ее состояние в "normal":
                active_button.state =  'normal'

                # Нажали на кнопку START, начинаем игру заново:
                if active_button.name == 'START':
                    self.__init__()
                    self.state = 'GAME'

                # На паузе и нажали CONTINUE, переведем игру с состояние GAME:
                elif active_button.name == 'CONTINUE':
                    self.state = 'GAME'

                # Нажали на QUIT - завешим работу приложения:
                elif active_button.name == 'QUIT':
                    pygame.quit()


    def draw_scene(self):
        # Выполняем заливку фона:
        self.screen.fill(BLACK)
        self.screen.blit(self.background_img, [0, 0])
        if self.state == 'START':
            # Рисуем только главное меню:
            self.main_menu.draw(self.screen)

        elif self.state == 'GAME':
            # Рисуем все спрайты в игре:
            self.top_panel.draw(self.screen)
            self.all_sprite_list.draw(self.screen)

        elif self.state == 'PAUSE':
            # Рисуем "обстановку" - платформы и главное меню:
            self.top_panel.draw(self.screen)
            self.platform_list.draw(self.screen)
            self.main_menu.draw(self.screen)

        elif self.state == 'FINISH':
            # Рисуем только главное меню:
            self.main_menu.draw(self.screen)

    def run(self):
        done = False
        # Запустили главный игровой цикл:
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                # Обрабатываем события для разных состояний:
                self.handle_scene(event)

            # Если идет игра, обновляем все объекты в игре:
            if self.state == 'GAME':
                self.all_sprite_list.update()
                self.top_panel.update(coin=self.player.score)
                # Проверяем, не досиг ли персонаж выхода:
                if self.player.rect.x > WIN_WIDTH - 70 and self.player.rect.y > WIN_HEIGHT - 70:
                    self.state = 'FINISH'

            # Если игра на паузе или на старте, обновляем  меню:
            else:
                self.main_menu.update()
            # Отрисовываем окно игры для текущего состояния:
            self.draw_scene()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

game = Game()
game.run()
