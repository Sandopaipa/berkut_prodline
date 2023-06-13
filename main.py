from states import ConveyorStates, SensorStates, RobotStates
from objects.sensors import DigitalSensor, OperatorButton
from objects.executors import Robot, Conveyor

import time
import threading


start_event = threading.Event()
stop_event = threading.Event()
system_start_event = threading.Event()
conveyor_finished_event = threading.Event()


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

def wait_for_operator(system_start_event):
    op_start_btn = OperatorButton()
    op_start_btn.activate()
    while not system_start_event.is_set():
        """
        Пока не была нажата кнопка оператора - 
        пока не возникло событие system_start_event -
        чекаем статус кнопки/
        Если кнопка была нажата - вызывается событие
        """
        if op_start_btn.state == SensorStates.__ON__:
            system_start_event.set()


if __name__ == '__main__':
    line = Conveyor()
    cell = LinkedList()
    for i in cell:
        cell.add()

    op_btn_thread = threading.Thread(
        target=wait_for_operator,
        args=(system_start_event,)
    )
    op_btn_thread.start()

    if system_start_event.is_set():
        for robot in cell:
            robot.robot.change_state(RobotStates.__WAITING__)

        while not conveyor_finished_event.is_set():
            line.work()
            if line.get_state() == ConveyorStates.__WAITING__:
                conveyor_finished_event.set()

    if conveyor_finished_event.is_set():
        for node in cell:
            if node.sensor.get_state() == SensorStates.__ON__:
                node.robot.work()


