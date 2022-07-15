import sys
from collections import Counter


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    msg_len = len(data[0])
    oxygen_data = data[:]
    scrub_data = data[:]
    for pos in range(msg_len):
        if not isinstance(oxygen_data, int):
            res = Counter(''.join([word[pos] for word in oxygen_data]))
            res = '1' if len(set(res.values())) == 1 else max(res, key=res.get)
            _new_data = [word for word in oxygen_data if word[pos] == res]
            if _new_data:
                oxygen_data = _new_data
            if not _new_data or len(oxygen_data) == 1:
                oxygen_data = int(oxygen_data[0], 2)

        if not isinstance(scrub_data, int):
            res = Counter(''.join([word[pos] for word in scrub_data]))
            res = '0' if len(set(res.values())) == 1 else min(res, key=res.get)
            _new_data = [word for word in scrub_data if word[pos] == res]
            if _new_data:
                scrub_data = _new_data
            if not _new_data or len(scrub_data) == 1:
                scrub_data = int(scrub_data[0], 2)

        if isinstance(oxygen_data, int) and isinstance(scrub_data, int):
            break
    print(oxygen_data * scrub_data)


if __name__ == '__main__':
    sys.exit(main())
