import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    data = [int(x)
            for row in data
            for x in row.split(',')]

    for i in range(80):
        old_fish = [(x - 1) if x > 0 else 6 for x in data]
        new_fish = [8] * data.count(0)
        data = old_fish + new_fish

    print(len(data))


if __name__ == '__main__':
    sys.exit(main())
