import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    data = [int(x)
            for row in data
            for x in row.split(',')]

    fish_per_day = {index: data.count(index) for index in range(0, 9)}

    for i in range(256):
        fish_per_day = {day: (fish_per_day[day + 1]
                              if day not in [8, 6]
                              else (fish_per_day[0]
                                    if day == 8
                                    else fish_per_day[7] + fish_per_day[0]))
                        for day in fish_per_day.keys()}
    print(sum(fish_per_day.values()))


if __name__ == '__main__':
    sys.exit(main())
