from states import RobotStates, ConveyorStates
import time


class Robot:
    def __init__(self, initial_state=RobotStates.__INIT__):
        self.state = initial_state

    def work(self):
        """
        По аналогии с конвйером - в качестве программы работы
        будет использоваться обычный таймер.
        """
        self.change_state(RobotStates.__WORKING__)
        print('Робот начал работу')
        time.sleep(10)
        print('Робот окончил работу')
        self.change_state(RobotStates.__WAITING__)

    def get_state(self):
        print('Робот:', self.state)
        time.sleep(1)
        return self.state

    def change_state(self, new_state):
        self.state = new_state


class Conveyor:

    def __init__(self, init_state=ConveyorStates.__INIT__):
        self.state = init_state

    def get_state(self):
        time.sleep(2)
        print(self.state)
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

        self.change_state(new_state=ConveyorStates.__WORKING__)
        print('Конвейер начал работу')
        time.sleep(5)
        print("Конвейер завершил работу")
        self.change_state(new_state=ConveyorStates.__WAITING__)
