from __future__ import print_function

import sys
from time import sleep

from PodSixNet.Connection import connection, ConnectionListener
from Whiteboard import Whiteboard

class Client(ConnectionListener, Whiteboard):
    def __init__(self, host, port):
        self.Connect((host, port))
        # храним в словаре всех игроков, которые подключены:
        self.players = {}
        # вызываем конструктор окна приложения:
        Whiteboard.__init__(self)
    
    def Loop(self):
        # Метод Pump() запрашивает канал подключения о новых событиях
        # Если какие-то события произошли, то он вызывает обратные вызовы Network_
        self.Pump()
        connection.Pump()
        self.Events()
        self.Draw([(self.players[p]['color'], self.players[p]['lines']) for p in self.players])
        
        if "connecting" in self.statusLabel:
            self.statusLabel = "connecting" + "".join(["." for s in range(int(self.frame / 30) % 4)])

    #####################################################
    # Обработчики событий
    def PenDown(self, e):
        connection.Send({"action": "startline", "point": e.pos})
    
    def PenMove(self, e):
        connection.Send({"action": "drawpoint", "point": e.pos})
    
    def PenUp(self, e):
        connection.Send({"action": "drawpoint", "point": e.pos})

    #####################################################
    # Специфичные для сети обратные вызовы
    # Названия таких  методы должны начинаться с Network_

    # Метод вызывает каждый раз, когда от сервера призодит сообщения вида:
    #  {"action": "initial", data }
    def Network_initial(self, data):
        # сообщение
        # print('Network_inital', data['lines'])
        # записать информцию об игроках (id, цвет и список нарисованных точек)
        self.players = data['lines']

    # Метод вызывает каждый раз, когда от сервера призодит сообщения вида:
    #  {"action": "drawpoint", data }
    def Network_drawpoint(self, data):
        # добавить к списку нарисованных точек новую точку data['point']
        # точку добавляем в список lines игрока с указанным id
        self.players[data['id']]['lines'][-1].append(data['point'])

    # Метод вызывает каждый раз, когда от сервера призодит сообщения вида:
    #  {"action": "startline", data }
    def Network_startline(self, data):
        self.players[data['id']]['lines'].append([data['point']])

    # Метод вызывает каждый раз, когда изменяется количество игроков
    # (добавляется новый игрок или удаляется существующий)
    # При этом от сервера приходит сообщения вида:
    # {"action": "players", 'players' : {....} }
    def Network_players(self, data):
        # указываем в строке состояния количество игроков
        print('PLAYERS', data)
        self.playersLabel = str(len(data['players'])) + " players"
        # создаем список mark -  ID клиентов, которые отключились
        mark = []
        for i in data['players']:
            if not i in self.players:
                # игрока из списка на сервере, еще нет в списке игроков клиента, добавляем:
                self.players[i] = {'color': data['players'][i], 'lines': []}
        for i in self.players:
            # игрок из списка клиента отсутствует в списке сервера,
            # помещаем его в список на удаление:
            if not i in data['players'].keys():
                mark.append(i)
        # удаляем из списка игроков всех отключившихся:
        for m in mark:
            del self.players[m]
    
    def Network(self, data):
        #print('network:', data)
        pass

    # Метод вызывается, когда установлено соединение с сервером
    # В этом случае от сервера призодит сообщения вида:
    #  {"action": "connected", data }
    def Network_connected(self, data):
        self.statusLabel = "connected"

    # Метод вызывает каждый раз, когда произошла ошибка
    # В этом случаеот сервера призодит сообщения вида:
    # {"action": "error", data }
    def Network_error(self, data):
        print('ERROR', data)
        import traceback
        traceback.print_exc()
        # вывести информацию об ошибке в строку состояния:
        self.statusLabel = data['error'][1]
        # в случае ошибки закрыть соединение
        connection.Close()


    # Метод вызывает , когда происходит потеря соединения
    # В этом случае от сервера призодит сообщения вида:
    #  {"action": "disconected", data }
    def Network_disconnected(self, data):
        # вывести информацию о разъединении в строку состояния:
        self.statusLabel += " - disconnected"

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "host:port")
        print("e.g.", sys.argv[0], "localhost:31425")
    else:
        host, port = sys.argv[1].split(":")
        c = Client(host, int(port))
        while 1:
            c.Loop()
            sleep(1/25)

