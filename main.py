from collections.abc import Iterable

from states import SensorStates, BaseExecutorState
from objects.sensors import DigitalSensor, OperatorButton
from objects.executors import Robot, Conveyor
import threading


start_event = threading.Event()
stop_event = threading.Event()
alarm_event = threading.Event()
system_work = threading.Event()
conveyor_work_event = threading.Event()
conveyor_finish_event = threading.Event()
robot_work_event = threading.Event()


class LinkedList:

    class Node:
        def __init__(self):
            self.sensor = DigitalSensor()
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
            yield current_node
            current_node = current_node.nextnode

    def list_count(self):
        print(self.count)
        return self.count

def robot_check(object, start_event, alarm_event):
    while True:
        for robot in object:
            if robot.robot.get_state() == BaseExecutorState.__ALARM__\
                or robot.robot.get_state() == None:
                print("Завершение работы: авария")
                alarm_event.set()
                break

def start_button_check(work, button):
    """
    Ожидание нажатие кнопки оператора для запуска работы
    производственной системы.
    """
    #Тестовое активирование кнопки
    button.activate()
    while not work.is_set():
        if button.state == SensorStates.__ON__:
            print('Система стартовала')
            work.set()

def alarm_button_check(alarm_event, button):
    """
    Ожидание нажатия кнопки сброса аварийной ситуации.
    """
    while alarm_event.is_set():
        if button.state == SensorStates.__ON__:
            print('Состояние аварии было сброшено')
            alarm_event.clear()
            system_work.clear()


def object_work(object_work_event, object_finish_event, object):
    object_work_event.set()
    object.work()
    if object.get_state() == BaseExecutorState.__WAITING__:
        object_work_event.clear()
        object_finish_event.set()
        print('---------------------Конвейеер закончил работу--------------------------------')

def robot_work(conveyor_finish_event, object):
    if conveyor_finish_event.is_set():
        conveyor_finish_event.clear()
        for robot in object:
            if robot.sensor.get_state() == SensorStates.__ON__:
                robot.robot.work()
                print("-------------------Робот начал работу-----------------------")
            else:
                print('Нет детали')
        robot_chain_check(object)


def robot_chain_check(object):
    all_works_finished_flag = False
    while all_works_finished_flag == False:
        work_finished = 0
        for robot in object:
            if robot.robot.get_state() == BaseExecutorState.__WAITING__:
                work_finished += 1
        if work_finished == object.list_count():
            all_works_finished_flag = True
            print('all robot finished all works')

def object_init(object):
    if isinstance(object, Iterable):
        try:
            for i in object:
                i.change_state(BaseExecutorState.__INIT__)
        except:
            pass
    else:
        try:
            object.change_state(BaseExecutorState)
        except:
            pass

def alarm_handler(object, event, *threads):
    alarm_button_check(button=object, alarm_event=event)
    for thread in threads:
        thread.stop()

def stop_working_threads(*threads):
    for thread in threads:
        thread._stop()

def set_alarm_behavour():
    line.alarm_handler()
    for i in cell:
        i.robot.alarm_handler()

def alarm_check(event, *threads):
    if event.is_set():
        stop_working_threads(*threads)
        print('ALARM ALL THREADS HAVE BEEN STOPPED')




if __name__ == '__main__':
    count = 3
    robot_check_interval = 1
    start_button = OperatorButton()
    alarm_button = DigitalSensor()
    # Экземпляр конвейера
    line = Conveyor()
    # Экземпляр цепочки технологических этапов
    cell = LinkedList()

    for i in range(0, 5):
        cell.add()

    for i in cell:
        i.sensor.state = SensorStates.__ON__


    robot_check_thread = threading.Timer(
        interval=robot_check_interval,
        function=robot_check,
        args=(
            cell,
            system_work,
            alarm_event,
        )
    )

    robot_check_thread.start()

    while True:

        if not system_work.is_set():
            start_button_check(system_work, start_button)

        conveyor_work_thread = threading.Thread(
            target=object_work,
            args=(system_work, conveyor_finish_event, line,)
        )
        robot_work_thread = threading.Thread(
            target=robot_work,
            args=(conveyor_finish_event, cell)
        )
        alarm_check_thread = threading.Thread(
            target=alarm_check,
            args=(alarm_event, conveyor_work_thread, robot_work_thread,)
        )
        alarm_check_thread.start()


        if count > 3:
            alarm_event.set()
        count += 1

        if not alarm_event.is_set():
            conveyor_work_thread.start()
            conveyor_work_thread.join()
            robot_work_thread.start()
            robot_work_thread.join()

        else:
            set_alarm_behavour()
            alarm_button_check(alarm_event, alarm_button)






















