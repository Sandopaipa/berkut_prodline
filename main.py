import time

from states import SensorStates, BaseExecutorState
from objects.sensors import DigitalSensor, OperatorButton
from objects.executors import Conveyor
import threading
from prodlines.berkut_prodline.ProdLine import SerialProdline


start_event = threading.Event()
stop_event = threading.Event()
alarm_event = threading.Event()
system_work = threading.Event()
conveyor_work_event = threading.Event()
conveyor_finish_event = threading.Event()
robot_work_event = threading.Event()


def robot_check(robots, timeout):
    """
    Фнукция, которая осуществляет постоянный опрос
    исполнительных механизмов.
    Если состояние исполнительного механзма - "АВАРИЯ" или
    не было получено в течение заданного времени -
    выставляется событие аварии.
    """
    global alarm_event
    while True:
        for robot in robots:
            start_time = time.time()
            if robot.robot.get_state() == BaseExecutorState.__ALARM__\
                    or robot.robot.get_state() is None\
                    or time.time() - start_time > timeout:
                alarm_event.set()
                break
            else:
                continue


def robot_chain_check(robots):
    """
    Функция, которая проверяет, все ли ИМ (на участке которых
    присутствует деталь) закончили свою работу и находятся в состоянии ожидания.
    Если все ИМ закончили свою работу - выставляет событие окончания работы ИМ
    """

    all_works_finished_flag = False
    while all_works_finished_flag is False:
        work_finished = 0
        for robot in robots:
            if robot.robot.get_state() == BaseExecutorState.__WAITING__:
                work_finished += 1
        if work_finished == prod_chain.count_working_sensors():
            all_works_finished_flag = True


def start_button_waiting(button):
    """
    Ожидание нажатия кнопки оператора для запуска работы
    производственной системы.
    """
    global system_work

    while not system_work.is_set():
        if button.state == SensorStates.__ON__:
            system_work.set()


def alarm_button_waiting(button):
    """
    Ожидание нажатия кнопки сброса аварийной ситуации.
    Если нажатие было зарегистрировано - то событие аварии
    снимается вместе с состоянием работы системы.
    """
    global alarm_event
    global start_button
    button.activate()
    while alarm_event.is_set():
        if button.state == SensorStates.__ON__:
            alarm_event.clear()
            system_work.clear()
            if start_button.get_state() == SensorStates.__ON__:
                start_button.deactivate()


def conveyor_work(conveyor):
    """
    функция, которая вводит конвейер в работу
    """
    global conveyor_work_event
    global conveyor_finish_event

    conveyor.work()
    if conveyor.get_state() == BaseExecutorState.__WAITING__:
        conveyor_work_event.clear()
        conveyor_finish_event.set()


def robots_work(robots):
    """
    Функция, которая вводит исполнительные механизмы
    в работу.
    """
    global conveyor_finish_event

    if conveyor_finish_event.is_set():
        conveyor_finish_event.clear()
        for robot in robots:
            if robot.sensor.get_state() == SensorStates.__ON__:
                robot.robot.work()
            else:
                continue
        robot_chain_check(robots)


def set_working_objects_alarm_behavour():
    """
    Функция включает режим аварийного поведения у
    всех работающих объектов
    """
    line.alarm_handler()
    for item in prod_chain:
        item.robot.alarm_handler()


def alarm_thread_stop(*threads):
    """
    Функция, останавливающая потоки в случае аварии
    """
    global alarm_event
    if alarm_event.is_set():
        for thread in threads:
            thread._stop()


if __name__ == '__main__':

    timeout = 5
    start_button = OperatorButton()
    alarm_button = OperatorButton()

    line = Conveyor()
    prod_chain = SerialProdline()

    robot_check_thread = threading.Thread(
        target=robot_check,
        args=(prod_chain, timeout)
    )
    robot_check_thread.start()

    while True:

        if not system_work.is_set():
            start_button_waiting(start_button)

        conveyor_work_thread = threading.Thread(
            target=conveyor_work,
            args=(line,)
        )
        robot_work_thread = threading.Thread(
            target=robots_work,
            args=(prod_chain,)
        )
        alarm_check_thread = threading.Thread(
            target=alarm_thread_stop,
            args=(conveyor_work_thread, robot_work_thread)
        )
        alarm_check_thread.start()

        for thread in [conveyor_work_thread, robot_work_thread]:
            if not alarm_event.is_set():
                thread.start()
                thread.join()
            else:
                set_working_objects_alarm_behavour()
                alarm_button_waiting(alarm_button)
                break
