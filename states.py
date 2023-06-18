from enum import Enum


class SensorStates(Enum):
    __ON__ = 'Активирован'
    __OFF__ = 'Не активен'


class BaseExecutorState(Enum):
    __INIT__ = 'Инициализирован'
    __WORKING__ = 'Работает'
    __WAITING__ = 'В ожидании'
    __ALARM__ = 'Авария'
