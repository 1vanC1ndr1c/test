import itertools
import os
import sys
from pathlib import Path


def machine(input_path):
    with open(input_path) as file:
        input_data = [x.strip() for x in file.readlines()]

    input_elements = input_data[0].split(',')
    triggers = input_data[1].split(',')
    acceptable = input_data[2].split(',')
    initial = input_data[3]

    graph = {k: v for k, v in [state.split('->') for state in input_data[4:]]}
    visited = depth_first_search(graph, initial, set(), triggers)

    state_groups = [[el for el in input_elements if el in acceptable],
                    [el for el in input_elements if el not in acceptable]]

    while True:
        changed = False
        for column_cnt, group in enumerate(state_groups):
            for i in group:
                first = True
                _tmp = []

                for j in group[group.index(i):len(group)]:

                    for trigger in triggers:
                        a = graph.get(f'{i},{trigger}')
                        b = graph.get(f'{j},{trigger}')

                        if a != b:
                            if not any([a in state_group
                                        and b in state_group
                                        for state_group in state_groups]):
                                changed = True
                                state = j if i < j else i
                                _tmp.append(state)
                                group.remove(state)
                                if first:
                                    state_groups.append(_tmp)
                                    first = False
                                break
            column_cnt += 1

        if not changed:
            break

    state_groups = sorted(state_groups)
    konLista = [el[0] for el in state_groups if el]

    parsed_dict = {states: collection[0]
                   for collection in state_groups
                   if collection
                   for states in collection[1:]}
    konDict = {}

    for key in graph:
        if key.split(',')[0] not in parsed_dict:
            if graph.get(key) in parsed_dict:
                konDict[key] = parsed_dict.get(graph.get(key))
            else:
                konDict[key] = graph.get(key)

    konLista = [x for x in konLista if x in visited]

    acceptable = [x for x in acceptable
                  if x not in [k.split(',')[0] for k in parsed_dict.keys()]
                  and x in visited]

    if initial in parsed_dict:
        initial = parsed_dict.get(initial)

    ret_stuff = [','.join(konLista),
                 ','.join(triggers),
                 ','.join(acceptable),
                 initial]

    for key in konDict:
        if key.split(',')[0] in visited:
            ret_stuff.append(f'{key}->{konDict.get(key)}')

    return ret_stuff


def depth_first_search(graph, start_node, visited, triggers):
    visited.add(start_node)

    keys = [f'{x[0]},{x[1]}'
            for x in list(itertools.product([start_node], triggers))]
    nodes = set([graph.get(k) for k in keys])

    for next_ in nodes - visited:
        depth_first_search(graph, next_, visited, triggers)
    return visited


def main():
    test_dir = Path(__file__).parent.resolve() / 'tests'
    for test in sorted(os.listdir(test_dir)):
        path_test = test_dir / test
        input_path = path_test / 't.ul'
        output_path = path_test / 't.iz'
        machine_solution = machine(input_path)
        with open(output_path) as file:
            expected_solution = [x.strip() for x in file.readlines()]

        print(f'Test={test}, Okay={expected_solution == machine_solution}')


if __name__ == '__main__':
    sys.exit(main())
