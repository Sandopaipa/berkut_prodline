from states import SensorStates

class DigitalSensor:
    """
    Цифровой сенсор, который имеет только два состояния:
    включен или выключен.
    """
    def __init__(self, init_state=SensorStates.__OFF__):
        self.name = 'default_sensor_name'
        self.state = init_state

    def get_state(self):
        return self.state


class OperatorButton(DigitalSensor):
    """
    Кнопка. Может быть либо включена - либо выключена.
    """
    def activate(self):
        self.state = SensorStates.__ON__
        return

    def deactivate(self):
        self.state = SensorStates.__OFF__

