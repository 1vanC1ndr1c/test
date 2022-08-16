import os
import sys


def main():
    with open('env', 'r') as file:
        env = [l.strip() for l in file.readlines()]

    env = [l.split('=', maxsplit=1) for l in env]

    for e in env:
        name, value = e
        os.environ[name] = value


if __name__ == '__main__':
    sys.exit(main())
