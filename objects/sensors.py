from states import SensorStates
import time

class DigitalSensor:
    def __init__(self, init_state=SensorStates.__OFF__):
        self.name = 'default_sensor_name'
        self.state = init_state

    def get_state(self):
        print('Сенсор:', self.state)
        time.sleep(1)
        return self.state




class OperatorButton(DigitalSensor):
    """
    Кнопка для запуска процесса работы
    ON - Начинается работа
    OFF - Заканчивается работа (не пауза)
    """
    def activate(self):
        self.state = SensorStates.__ON__
        return

class OperatorInitButton(DigitalSensor):
    """
    Кнопка для сброса аварии
    ON - возвращает систему в состояние инициализации
    OFF - значение принимается автоматически.
    """
    def system_init(self):
        if self.state == SensorStates.__ON__:
            self.state = SensorStates.__OFF__
        else:
            self.state = SensorStates.__ON__