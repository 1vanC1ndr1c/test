import os
import sys
from pathlib import Path


def machine(input_path):
    with open(input_path) as file:
        input_data = [x.strip() for x in file.readlines()]

    input_symbols = input_data[0].split('|')
    acceptable = input_data[4]
    initial_state = input_data[5]
    initial_stack_sign = input_data[6]
    graph = {k: v for k, v in [state.split('->') for state in input_data[7:]]}

    init = '|'.join([f'{initial_state}#{initial_stack_sign}'])
    solution_all = []

    for in_symbol in input_symbols:
        in_symbol = in_symbol.replace(',', '')
        stack_sign = initial_stack_sign
        current_state = initial_state
        solution = find_solution(in_symbol,
                                 stack_sign,
                                 current_state,
                                 graph,
                                 acceptable)
        solution_all.append(init + solution)
    return solution_all


def find_solution(in_symbol, stack_sign, current_state, graph, acceptable):
    solution = ''
    while True:
        if not len(in_symbol) > 0:
            return solution

        stack_symbol = stack_sign[0] if len(stack_sign) > 1 else stack_sign
        key = f'{current_state},{in_symbol[0]},{stack_symbol}'
        empty_state = f'{(split := key.split(","))[0]},$,{split[2]}'

        if key in graph or empty_state in graph:

            if in_symbol == '$' and current_state in acceptable:
                return solution + '|1'

            value = graph.get(key) or graph.get(empty_state)

            q_state = value.split(',')
            stack_sign = stack_sign[1:]
            stack_sign = q_state[1] + stack_sign

            if stack_sign[0] == '$':
                stack_sign = stack_sign.replace('$', '')
                stack_sign = '$' if not stack_sign else stack_sign

            current_state = q_state[0]

            in_symbol = in_symbol[1:] if key in graph else in_symbol
            in_symbol = '$' if not in_symbol else in_symbol
            solution += f'|{current_state}#{stack_sign}'

        elif in_symbol == '$':
            solution += '|1' if current_state in acceptable else '|0'
            return solution
        else:
            return solution + '|fail|0'


def main():
    test_dir = Path(__file__).parent.resolve() / 'tests'
    for test in sorted(os.listdir(test_dir)):
        path_test = test_dir / test
        input_path = path_test / 'primjer.in'
        output_path = path_test / 'primjer.out'
        machine_solution = machine(input_path)
        with open(output_path) as file:
            expected_solution = [x.strip() for x in file.readlines()]

        print(f'Test={test}, Okay={expected_solution == machine_solution}')


if __name__ == '__main__':
    sys.exit(main())
