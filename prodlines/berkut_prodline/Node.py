from objects.sensors import DigitalSensor
from objects.executors import Robot


class Node:
    """
    Узел - или технологический этап производственной линии.
    """
    def __init__(self):
        self.sensor = DigitalSensor()
        self.robot = Robot()
        self.nextnode = None
        self.node_id = 1
