from prodlines.berkut_prodline.Node import Node
from states import SensorStates


class SerialProdline:
    """
    Последовательная производственная линия.
    """
    def __init__(self):
        self.head = None
        self.count = 0

    def add(self):
        """
        Метод для добавления новых узлов в производственную линию.
        """
        new_node = Node()
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

    def count_working_sensors(self):
        """
        Метод для получения количества активных концевых выключателей.
        """
        working_nodes_number = 0
        current_node = self.head
        while current_node is not None:
            if current_node.sensor.get_state() == SensorStates.__ON__:
                working_nodes_number += 1
            current_node = current_node.nextnode
        return working_nodes_number

