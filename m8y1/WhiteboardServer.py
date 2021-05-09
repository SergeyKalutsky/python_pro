import sys
from time import sleep

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

# Описание канала сервера для одного подключенного клиента.
class ServerChannel(Channel):
    # конструктор класса, создание нового подключения
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        # Назначаем ID для нового клиента:
        self.id = str(self._server.NextId())
        intid = int(self.id)
        # Назначаем цвет для нового клиента
        self.color = [(intid + 1) % 3 * 84, (intid + 2) % 3 * 84, (intid + 3) % 3 * 84]
        # Список всех линий, нарисованных клиентом
        self.lines = []
    
    # передать информацию от сервера всем остальным клиентам
    def PassOn(self, data):
        # обновить данные в data. Задать id  значением self.id
        data.update({"id": self.id})
        print('PassOn', data)
        print(self.id)
        # передать сообщение data, всем подключенным клиентам
        self._server.SendToAll(data)
    
    # при закрытии канала с клиентом, удалить игрока
    def Close(self):
        self._server.DelPlayer(self)
        print('del', self)
    
    #####################################################
    # Специфичные для сети обратные вызовы
    # Названия таких  методы должны начинаться с Network_

    # Метод вызывается, когдаклиент начал рисовать линию
    # В этом случае от клиента призодит сообщения вида:
    #  {"action": "startline", "point": .... }
    def Network_startline(self, data):
        # добавить в список нарисованных кривых  новую,
        # поместить в список точек этой кривой позицию point:
        self.lines.append([data['point']])
        # отправить информацию о рисовании всем клиентам:
        # при этом на стороне клиента будет вызван метод Network_startline
        self.PassOn(data)

    # Метод вызывается, когда клиент продолжает рисовать линию
    # В этом случае от клиента призодит сообщения вида:
    #  {"action": "drawpoint", "point": e.pos}
    def Network_drawpoint(self, data):
        # добавить в список точек текущей кривой (lines[-1]) еще одну точку point:
        self.lines[-1].append(data['point'])
        # отправить информацию о рисовании всем клиентам:
        # при этом на стороне клиента будет вызван метод Network_drawpoint
        self.PassOn(data)

# Описание работы сервера
class WhiteboardServer(Server):
    channelClass = ServerChannel
    
    def __init__(self, *args, **kwargs):
        # ведет отсчет ID для назначения их новым подключениям
        self.id = 0
        Server.__init__(self, *args, **kwargs)
        # создать словарь для хранения иформации об игроках:
        self.players = dict()
        print('Server launched')

    # Перейти к следующему номеру ID для следующего подключения
    def NextId(self):
        self.id += 1
        return self.id

    #  Метод вызывается, когда установлено
    #  соединение с новым клиентом
    def Connected(self, channel, addr):
        # Добавить нового игрока
        self.AddPlayer(channel)

    # Метод для добавлениея нового игрока на сервер
    # player - это информация о канале, устанвленном между сервером и новым клиентом
    def AddPlayer(self, player):
        # Вывести информацию о подключении игрока
        print("New Player" + str(player.addr) + " " + str(player))
        # Добавить в словарь players информацию о новом соединении:
        self.players[player] = True
        # отправить по каналу игрока информацию о уже нарисованных в игре кривых:
        lines = dict([(p.id, {"color": p.color, "lines": p.lines}) for p in self.players])
        player.Send({"action": "initial", "lines": lines})
        # player.Send({"action": "initial", "lines": dict([(p.id, {"color": p.color, "lines": p.lines}) for p in self.players])})
        # отправить всем игрокам информацию об обновленном количестве игроков:
        self.SendPlayers()
    
    # Метод удаляет игрока при его отключении от сервера
    def DelPlayer(self, player):
        print("Deleting Player" + str(player.addr))
        # удалить из словаря players запись об этом канале связи:
        self.players.pop(player)
        # отправить всем игрокам информацию об обновленном количестве игроков:
        self.SendPlayers()

    # Метод рассылает всем игрокам информацию о существующих на сервере подключениях:
    def SendPlayers(self):
        self.SendToAll({"action": "players", "players": dict([(p.id, p.color) for p in self.players])})
    
    # Метод рассылает сообщение data всем подключенным клиентам:
    def SendToAll(self, data):
        for p in self.players:
            p.Send(data)

    # Запуск сервера. Проверяет наличие новых сообщений от клиентов каждые 0.0001 сек
    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

# get command line argument of server, port
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "host:port")
        print("e.g.", sys.argv[0], "localhost:31425")
    else:
        host, port = sys.argv[1].split(":")
        s = WhiteboardServer(localaddr=(host, int(port)))
        s.Launch()

