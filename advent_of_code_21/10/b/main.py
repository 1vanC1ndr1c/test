import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    open_brackets = ['(', '{', '[', '<']
    closed_brackets = [')', '}', ']', '>']
    scores = []
    score_lookup = {')': 1, ']': 2, '}': 3, '>': 4}

    for line in data:
        line_corrupted = False
        line_open = []
        for c in line:
            if c in open_brackets:
                line_open.append(c)
                continue

            last_open = line_open.pop()
            expected_closed = closed_brackets[open_brackets.index(last_open)]

            if expected_closed != c:
                line_corrupted = True
                break

        if line_corrupted:
            continue

        needed_closers = [closed_brackets[open_brackets.index(x)]
                          for x in line_open[::-1]]

        scores.append(sum(
            [5 ** (len(needed_closers) - i - 1) * score_lookup[el]
             for i, el in enumerate(needed_closers)]))

    print(sorted(scores)[int(len(scores) / 2)])


if __name__ == '__main__':
    sys.exit(main())
