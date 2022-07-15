import itertools
import math
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

    print(math.prod(sorted(
        [len(_get_neighbors(k[0], k[1], data, {})) for k, v in mins.items()],
        reverse=True
    )[:3]))


def _get_neighbors(x, y, coll, neighbor_vals):
    if not (0 <= y < len(coll)) or not (0 <= x < len(coll[0])):
        return neighbor_vals

    if (x, y) in neighbor_vals.keys() or coll[y][x] == 9:
        return neighbor_vals

    neighbor_vals[(x, y)] = coll[y][x]

    return {**neighbor_vals,
            **_get_neighbors(x - 1, y, coll, neighbor_vals),
            **_get_neighbors(x + 1, y, coll, neighbor_vals),
            **_get_neighbors(x, y - 1, coll, neighbor_vals),
            **_get_neighbors(x, y + 1, coll, neighbor_vals)}


if __name__ == '__main__':
    sys.exit(main())
