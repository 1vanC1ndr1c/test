import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    data = [int(el) for el in data]

    previous_sum = sum(data[:3])
    data = data[1:]
    bigger_counter = 0
    for index, el in enumerate(data):
        current_sum = sum(data[index:index + 3])
        if current_sum > previous_sum:
            bigger_counter += 1
        previous_sum = current_sum

    print(bigger_counter)


if __name__ == '__main__':
    sys.exit(main())
