from states import BaseExecutorState


class BaseExecutor:
    def __init__(self, initial_state=BaseExecutorState.__INIT__):
        self.state = initial_state

    def get_state(self):
        return self.state

    def change_state(self, new_state):
        self.state = new_state
        return self.state

    def work(self):
        pass

    def alarm_handler(self):
        """
        Метод для имлпементации аварийного завершения работы.
        """
        pass


class Robot(BaseExecutor):
    def work(self):
        """
        Метод передает необходимые команды в контроллер управления
        исполнительным механизмом для задания его работы.
        """
        self.change_state(BaseExecutorState.__WORKING__)
        self.change_state(BaseExecutorState.__WAITING__)

    def get_state(self):
        return self.state


class Conveyor(BaseExecutor):

    def get_state(self):
        return self.state

    def work(self):
        """
        Метод изменяет состояние объекта и "передает" команды
        на частотный преобразователь электропривода конвейера.
        """

        self.change_state(new_state=BaseExecutorState.__WORKING__)
        self.change_state(new_state=BaseExecutorState.__WAITING__)
