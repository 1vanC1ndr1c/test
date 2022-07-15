import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    data = tuple(tuple(int(el)
                       if el.isnumeric() else el
                       for el in row.split(' '))
                 for row in data)

    h_pos = v_pos = 0
    for direction, value in data:
        if direction == 'forward':
            h_pos += value
        elif direction == 'down':
            v_pos += value
        elif direction == 'up':
            v_pos -= value

    print(h_pos, v_pos)
    print(h_pos * v_pos)


if __name__ == '__main__':
    sys.exit(main())
