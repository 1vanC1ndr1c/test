import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    larger_counter = 0
    previous_value = int(data[0])
    for el in data[1:]:
        el = int(el)
        if el > previous_value:
            larger_counter += 1
        previous_value = el

    print(larger_counter)


if __name__ == '__main__':
    sys.exit(main())
