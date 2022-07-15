import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    data = [int(x)
            for row in data
            for x in row.split(',')]

    print(min([sum([abs(el - shift)
                    for el in data])
               for shift in range(max(data) + 1)]))


if __name__ == '__main__':
    sys.exit(main())
