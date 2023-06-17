from enum import Enum


class States(Enum):
    pass


class SensorStates(States):
    __ON__ = 'Активирован'
    __OFF__ = 'Не активен'


class BaseExecutorState(States):
    __INIT__ = 'Инициализирован'
    __WORKING__ = 'Работает'
    __WAITING__ = 'В ожидании'
    __ALARM__ = 'Авария'
