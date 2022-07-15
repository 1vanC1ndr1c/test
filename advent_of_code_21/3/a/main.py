import sys
from collections import Counter


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    gamma = ''
    for pos in range(len(data[0])):
        res = Counter(''.join([word[pos] for word in data]))
        res = max(res, key=res.get)
        gamma += res

    epsilon = int("".join(["1" if ch == "0" else "0" for ch in gamma]), 2)
    gamma = int(gamma, 2)
    print(epsilon * gamma)


if __name__ == '__main__':
    sys.exit(main())
