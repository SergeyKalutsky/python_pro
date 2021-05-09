import pygame

SCREENSIZE = (500, 500)


pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)

pygame.font.init()
fnt = pygame.font.SysFont("Arial", 14)
txtpos = (100, 90)

# Класс описывает основной интерфейс клиента
# Создает окно, вызывает обработчики событий и отрисовывает экран.
class Whiteboard:
    def __init__(self):
        # строка состояния
        self.statusLabel = "connecting"
        self.playersLabel = "0 players"
        self.frame = 0
        self.down = False

    # Обработка событий в окне клиента
    def Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
                pygame.quit()
                # exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.down = True
                # начало рисования, вызываем соответствующий метод клиента
                self.PenDown(event)
            
            if event.type == pygame.MOUSEMOTION and self.down:
                # во время рисования, вызываем соответствующий метод клиента
                self.PenMove(event)
            
            if event.type == pygame.MOUSEBUTTONUP:
                self.down = False
                # закончили рисовать, вызываем соответствующий метод клиента
                self.PenUp(event)
    
    # отрисовка на экране строки состояния и всех линий
    def Draw(self, linesets):
        # очищаем экран
        screen.fill([255, 255, 255])
        # выводим строку состояния
        txt = fnt.render(self.statusLabel, 1, (0, 0, 0))
        screen.blit(fnt.render(self.statusLabel, 1, (0, 0, 0)), [10, 10])
        txt = fnt.render(self.playersLabel, 1, (0, 0, 0))
        screen.blit(fnt.render(self.playersLabel, 1, (0, 0, 0)), [10, 20])

        for c, lines in linesets:
            # перебираем все наборы точек
            for l in lines:
                # для каждого набора точек l, соединяем их линиями заданным цветом c
                if len(l) > 1:
                    # рисуем последовательно смежные прямые сглаженные линий по заданному набору точек l
                    pygame.draw.aalines(screen, c, False, l)
        # обновляем изображение на экране
        pygame.display.flip()
        # переходим к следующему кадру
        self.frame += 1
