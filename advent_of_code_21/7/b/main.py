import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    data = [int(x)
            for row in data
            for x in row.split(',')]

    print(min([sum([sum(x for x in range(abs(el - shift) + 1))
                    for el in data])
               for shift in range(max(data) + 1)]))


if __name__ == '__main__':
    sys.exit(main())
