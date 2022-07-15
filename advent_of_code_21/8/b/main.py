import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    data = [row.split(' ') for row in data]
    data = [(row[:row.index('|')], row[row.index('|') + 1:]) for row in data]

    solution = 0
    for el in data:
        input_data = el[0]
        answer_mapping = {'x': []}
        for combo in input_data:
            if len(combo) == 2:
                answer_mapping[1] = set(list(combo))
            elif len(combo) == 4:
                answer_mapping[4] = set(list(combo))
            elif len(combo) == 3:
                answer_mapping[7] = set(list(combo))
            elif len(combo) == 7:
                answer_mapping[8] = set(list(combo))
            else:
                answer_mapping['x'].append(set(list(combo)))

        answer_mapping[9] = [x for x in answer_mapping['x']
                             if len(x) == 6
                             and answer_mapping[4].issubset(x)][0]
        answer_mapping[0] = [x for x in answer_mapping['x']
                             if len(x) == 6
                             and answer_mapping[7].issubset(x)
                             and not answer_mapping[4].issubset(x)][0]
        answer_mapping[6] = [x for x in answer_mapping['x']
                             if len(x) == 6
                             and not answer_mapping[7].issubset(x)
                             and not answer_mapping[4].issubset(x)][0]

        answer_mapping[5] = [x for x in answer_mapping['x']
                             if len(x) == 5
                             and x.issubset(answer_mapping[6])][0]
        answer_mapping[3] = [x for x in answer_mapping['x']
                             if len(x) == 5
                             and x.issubset(answer_mapping[9])
                             and not x.issubset(answer_mapping[6])][0]
        answer_mapping[2] = [x for x in answer_mapping['x']
                             if len(x) == 5
                             and not x.issubset(answer_mapping[9])
                             and not x.issubset(answer_mapping[6])][0]
        del answer_mapping['x']

        output_data = el[1]
        solution += int(''.join([str([k for k, v in answer_mapping.items()
                                      if v == set(list(combo))][0])
                                 for combo in output_data]))

    print(solution)


if __name__ == '__main__':
    sys.exit(main())
