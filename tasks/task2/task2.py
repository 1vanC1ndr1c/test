import sys
from pathlib import Path


def main():
    file_path = Path(__file__).resolve().parent / 'file1.txt'

    data = read(file_path)

    balanced = solution(data=data)

    if not balanced:
        print('un', end='')
    print('balanced')


def solution(data: str) -> bool:
    """
    Determine whether the containing text has balanced brackets.

    Args:
        data: data being checked

    Returns:
        True if balanced, False otherwise

    """

    bracket_matches = {'(': ')', '{': '}', '[': ']'}

    open_brackets = []
    for char in data:
        if char in bracket_matches.keys():
            open_brackets.append(char)

        elif char in bracket_matches.values():
            open_bracket = open_brackets.pop()
            if bracket_matches[open_bracket] != char:
                return False

    if open_brackets:
        return False

    return True


def read(file_path: Path) -> str:
    """
    Read a file

    Args:
        file_path: Path to the file being read

    Returns:
        The whole file represented in a string, empty string if the file
        does not exist
    """
    if not file_path.is_file():
        return ''

    with open(file_path, 'r') as file:
        data = file.read()

    return data


if __name__ == '__main__':
    sys.exit(main())
