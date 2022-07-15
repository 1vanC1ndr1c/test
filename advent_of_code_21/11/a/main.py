import itertools
import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()
    data = [list(int(y) for y in x) for x in data]

    flash_counter = 0
    for i in range(100):
        data = [[el + 1 for el in row] for row in data]
        data, new_flashes = flash_neighbors([[{'value': el, 'flashed': False}
                                              for el in row]
                                             for row in data])
        flash_counter += new_flashes
        data = [[0 if el > 9 else el for el in row] for row in data]

    print(flash_counter)


def flash_neighbors(data):
    needs_flashing = True
    new_data = data[:]
    internal_flash_counter = 0
    while needs_flashing:
        needs_flashing = False
        data = new_data[:]
        for y, row in enumerate(data):
            for x, el in enumerate(row):
                if el['value'] <= 9:
                    continue
                if el['flashed']:
                    continue

                internal_flash_counter += 1
                new_data[y][x]['flashed'] = True
                needs_flashing = True

                neighbor_coords = [item for item in
                                   itertools.product(
                                       range(x - 1, x + 2),
                                       range(y - 1, y + 2))
                                   if -1 < item[0] < len(row)
                                   and -1 < item[1] < len(data)]
                for coord in neighbor_coords:
                    new_data[coord[1]][coord[0]]['value'] += 1

    return ([[el['value'] for el in row] for row in data],
            internal_flash_counter)


def print_data(data):
    for row in data:
        print(row)


if __name__ == '__main__':
    sys.exit(main())
