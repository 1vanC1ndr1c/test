import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    open_brackets = ['(', '{', '[', '<']
    closed_brackets = [')', '}', ']', '>']
    high_score = 0
    score_lookup = {')': 3, ']': 57, '}': 1197, '>': 25137}
    for line in data:
        line_open = []
        for c in line:
            if c in open_brackets:
                line_open.append(c)
                continue

            last_open = line_open.pop()
            expected_closed = closed_brackets[open_brackets.index(last_open)]

            if expected_closed != c:
                high_score += score_lookup[c]
    print(high_score)


if __name__ == '__main__':
    sys.exit(main())
