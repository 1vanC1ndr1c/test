import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    data = [row.split(' ') for row in data]
    data = [(row[:row.index('|')], row[row.index('|') + 1:]) for row in data]
    data = sum([1 if len(combo) in [2, 3, 4, 7] else 0
                for el in data
                for combo in el[1]])
    print(data)


if __name__ == '__main__':
    sys.exit(main())
