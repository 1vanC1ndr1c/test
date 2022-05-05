import itertools
import sys


def machine(input_data):
    input_data = [line.strip() for line in input_data]

    states = input_data[0].split(',')
    symbols = input_data[1].split(',')
    acceptable = input_data[2].split(',')
    initial_state = input_data[3]
    graph = {k: v for k, v in [state.split('->') for state in input_data[4:]]}

    visited_states = depth_first_search(graph, initial_state, set(), symbols)

    state_groups = [acceptable, [x for x in states if x not in acceptable]]
    state_groups = traverse([x[:] for x in state_groups], symbols, graph)
    state_groups = sorted([x for x in state_groups if x[0] in visited_states])

    mapping = {state: x[0] for x in state_groups for state in x[1:]}

    connections = {key: (mapping.get(state)
                         if (state := graph.get(key)) in mapping
                         else state)
                   for key in graph
                   if key.split(',')[0] not in mapping}

    acceptable = [state for state in acceptable
                  if state not in [k.split(',')[0]
                                   for k in mapping.keys()]
                  and state in visited_states]

    initial_state = (mapping.get(initial_state)
                     if initial_state in mapping
                     else initial_state)

    transition_fn = [f'{key}->{connections.get(key)}'
                     for key in connections
                     if key.split(',')[0] in visited_states]

    solution = [','.join([grp[0] for grp in state_groups]),
                ','.join(symbols),
                ','.join(acceptable),
                initial_state] + transition_fn

    [print(x) for x in solution]


def depth_first_search(graph, start_node, visited, symbols):
    visited.add(start_node)
    keys = [f'{x[0]},{x[1]}'
            for x in list(itertools.product([start_node], symbols))]
    nodes = set([graph.get(k) for k in keys])
    for next_ in nodes - visited:
        depth_first_search(graph, next_, visited, symbols)
    return visited


def traverse(state_groups, symbols, graph):
    state_groups_prev = state_groups[:]
    for group in state_groups[:]:
        for grp_el in group:
            new_state_group = []
            for nxt_el in group[group.index(grp_el):len(group)]:
                for symbol in symbols:
                    el_value = graph.get(f'{grp_el},{symbol}')
                    nxt_value = graph.get(f'{nxt_el},{symbol}')
                    if el_value == nxt_value:
                        continue
                    if not any([el_value in state_group
                                and nxt_value in state_group
                                for state_group in state_groups]):
                        new_state_group.append(nxt_el
                                               if grp_el < nxt_el
                                               else grp_el)
                        break
            for state in new_state_group:
                group.remove(state)
            if new_state_group:
                state_groups.append(new_state_group)

    if state_groups_prev == state_groups:
        return [grp for grp in state_groups if grp]
    else:
        return traverse(state_groups, symbols, graph)


def main():
    input_data = sys.stdin.readlines()
    machine(input_data)


if __name__ == '__main__':
    sys.exit(main())
