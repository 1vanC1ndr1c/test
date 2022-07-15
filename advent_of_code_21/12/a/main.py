import itertools
import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    nodes = []
    for el in data:
        el_a, el_b = el.split('-')

        if el_a not in [x.value for x in nodes]:
            node_a = Node(el_a)
            nodes.append(node_a)
        else:
            node_a = [n for n in nodes if n.value == el_a][0]

        if el_b not in [x.value for x in nodes]:
            node_b = Node(el_b)
            nodes.append(node_b)
        else:
            node_b = [n for n in nodes if n.value == el_b][0]

        node_a.add_connection(node_b)
        node_b.add_connection(node_a)

    for el in nodes:
        print(f'Node={el.value}, '
              f'Connections={[n.value for n in el.connections]}')


class Node:
    def __init__(self, value):
        self.value = value
        self.connections = set()

    def add_connection(self, connection):
        self.connections.add(connection)


if __name__ == '__main__':
    sys.exit(main())
