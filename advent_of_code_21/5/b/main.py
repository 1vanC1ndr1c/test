import sys
from collections import defaultdict


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    ranges = [row.split('->') for row in data]
    ranges = [[el.strip().split(',') for el in row] for row in ranges]
    ranges = {index: row for index, row in enumerate(ranges)}
    ranges = {key: {'x': (int(value[0][0]), int(value[1][0])),
                    'y': (int(value[0][1]), int(value[1][1]))}
              for key, value in ranges.items()}
    ranges = {key: {xy: list(range(xy_val[0], xy_val[1] + 1)
                             if xy_val[0] < xy_val[1]
                             else reversed(range(xy_val[1], xy_val[0] + 1)))
                    for xy, xy_val in value.items()}
              for key, value in ranges.items()}
    ranges = {key: {'x': (value['x'] * len(value['y'])
                          if len(value['y']) > len(value['x'])
                          else value['x']),
                    'y': (value['y'] * len(value['x'])
                          if len(value['x']) > len(value['y'])
                          else value['y'])}
              for key, value in ranges.items()}
    ranges = {key: [(value['x'][i], value['y'][i])
                    for i in range(len(value['x']))]
              for key, value in ranges.items()}

    overlaps = defaultdict(list)
    for index, coords in ranges.items():
        for coord in coords:
            overlaps[coord].append(index)
    print(len([x for x in overlaps.values() if len(x) > 1]))


if __name__ == '__main__':
    sys.exit(main())
