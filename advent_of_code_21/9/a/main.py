import itertools
import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    data = [[int(x) for x in list(row)] for row in data]
    mins = {}
    for y, row in enumerate(data):
        surrounding_elements_y = list(range(y - 1, y + 2))
        for x, el_val in enumerate(row):
            surrounding_elements_x = list(range(x - 1, x + 2))

            neighbor_coords = list(itertools.product(surrounding_elements_x,
                                                     surrounding_elements_y))
            neighbor_coords = [item for item in neighbor_coords
                               if -1 < item[0] < len(row)
                               and -1 < item[1] < len(data)]

            neighbor_vals = {(x, y): data[y][x] for x, y in neighbor_coords}

            min_neighbor_val = min(neighbor_vals.values())

            if min_neighbor_val != el_val:
                continue

            mins[(x, y)] = el_val

            old_mins_coords = set(
                neighbor_coords).intersection(set(mins.keys()))

            for old_min_coord in old_mins_coords:
                old_min_val = mins[old_min_coord]
                if old_min_val > el_val:
                    del mins[old_min_coord]

    print(sum([x + 1 for x in mins.values()]))


if __name__ == '__main__':
    sys.exit(main())
