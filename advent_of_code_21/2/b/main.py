import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    data = tuple(tuple(int(el)
                       if el.isnumeric() else el
                       for el in row.split(' '))
                 for row in data)

    h_pos = v_pos = aim = 0
    for direction, value in data:
        if direction == 'forward':
            h_pos += value
            v_pos += aim * value
        elif direction == 'down':
            aim += value
        elif direction == 'up':
            aim -= value

    print(h_pos, v_pos)
    print(h_pos * v_pos)


if __name__ == '__main__':
    sys.exit(main())
