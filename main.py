from enum import Enum
import time
import threading


class States(Enum):
    pass


class SensorStates(States):
    __ON__ = 'Активирован'
    __OFF__ = 'Не активен'


class RobotStates(States):
    __WORKING__ = 'Работает'
    __WAITING__ = 'В ожидании'
    __ALARM__ = 'Авария'


class ConveyorStates(States):
    __WORKING__ = 'Работает'
    __WAITING__ = 'В ожидании'
    __ALARM__ = 'Авария'


class Sensor:
    def __init__(self, init_state=False):
        self.name = 'default_sensor_name'
        self.state = init_state

    def get_state(self):
        return self.state

    def toggle_state(self):
        if self.state == SensorStates.__ON__:
            self.state = SensorStates.__OFF__
        else:
            self.state = SensorStates.__ON__


class Robot:
    def __init__(self,
                 initial_state=RobotStates.__WAITING__,
                 init_tim_value=42):
        self.state = initial_state
        self.tim_value = init_tim_value

    def work(self):
        """
        По аналогии с конвйером - в качестве программы работы
        будет использоваться обычный таймер.
        """
        while self.get_state() != RobotStates.__ALARM__:
            self.change_state(RobotStates.__WORKING__)
            time.sleep(10)



    def stop(self):
        pass

    def get_state(self):
        return self.state

    def change_state(self, new_state):
        self.state = new_state

    def check(self):
        pass

    def alarm_handler(self):
        pass


class Conveyor:

    def __init__(self, init_state=ConveyorStates.__WAITING__):
        self.state = init_state

    def get_state(self):
        return self.state

    def change_state(self, new_state):
        self.state = new_state
        return self.state

    def work(self):
        """
        Изменяем состояние объекта и начинаем выполнение программы
        двигателя. Для примера - можно использовать таймер.
        Конвейер работает только, если он не в состоянии "АВАРИЯ".
        При этом - состояние конвейера может измениться "извне".
        """
        while self.get_state() != ConveyorStates.__ALARM__\
                and self.get_state() != ConveyorStates.__WAITING__:
            self.change_state(new_state=ConveyorStates.__WORKING__)
            time.sleep(10)
            print("Конвейер завершил работу")
            self.change_state(new_state=ConveyorStates.__WAITING__)




class LinkedList:

    class Node:
        def __init__(self):
            self.sensor = Sensor()
            self.robot = Robot()
            self.nextnode = None
            self.node_id = 1

    def __init__(self):
        self.head = None
        self.count = 0

    def add(self):
        new_node = self.Node()
        if self.head is None:
            self.head = new_node
            self.count += 1
            self.head.node_id = self.count
            return
        else:
            current_node = self.head
            while current_node.nextnode is not None:
                current_node = current_node.nextnode
            current_node.nextnode = new_node
            self.count += 1
            current_node.node_id = self.count
            return

    def __iter__(self):
        current_node = self.head
        while current_node is not None:
            yield current_node.node_id
            current_node = current_node.nextnode

    def list_count(self):
        return self.count

def add_some_nodes():
    a = LinkedList()
    a.add()
    a.add()
    a.add()

if __name__ == '__main__':

    add_some_nodes()
    line = Conveyor()
    thread1 = threading.Thread(line.work())
    thread2 = threading.Thread(line.get_state())

