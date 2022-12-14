import sys
from pathlib import Path
from typing import List, NamedTuple, Union


class FileDataEntry(NamedTuple):
    value: str
    value_id: str


class MatchedData(NamedTuple):
    name: str
    surname: str
    value_id: str

    def __str__(self):
        return f'{self.name} {self.surname} {self.value_id}'


def main():
    file_1_path = Path(__file__).resolve().parent / 'file1.txt'
    file_2_path = Path(__file__).resolve().parent / 'file2.txt'

    solution(names_file=file_1_path, surnames_file=file_2_path)


def solution(names_file: Path, surnames_file: Path):
    """
    Read two files and match the names found in one file with the surnames
    found in the other file by comparing corresponding IDs found in both files.

    Args:
        names_file: Path to the file containing rows of (name, id)
        surnames_file: Path to the file containing rows of (surname, id)

    """
    max_len = 1_000_000  # Extension 2
    offset = 0  # Extension 2
    while True:
        names_by_id = _read(names_file,
                            max_len=max_len,  # Extension 2
                            offset=offset)  # Extension 2
        if not names_by_id:  # Extension 2
            return  # Extension 2

        surnames_by_id = _read(surnames_file,
                               max_len=max_len,  # Extension 2
                               offset=offset)  # Extension 2
        if not surnames_by_id:  # Extension 2
            return  # Extension 2

        matches = list(_match_data(names_by_id, surnames_by_id))

        [print(match) for match in matches]

        offset += max_len  # Extension 2


def _read(file_path: Path,
          max_len=1_000,
          offset=0) -> List[Union[FileDataEntry, None]]:
    """
    Read file and return structured data if the file exists and if the
    validation is successful

    Args:
        file_path: Path to the file being read
        max_len: maximum number of lines to be read # Extension 2
        offset: Offset from the beginning of the file # Extension 2
    Returns:
        Rows of (value, id), if no error occurred

    """
    if not file_path.is_file():
        return []

    with open(file_path, 'r') as file:
        file.seek(offset)  # Extension 2
        data = file.read(max_len).splitlines()
        data = [item.split(' ') for item in data]

    if not _validate(data):
        return []

    data = [FileDataEntry(*item) for item in data]

    return data


def _validate(data: List) -> bool:
    # Napomena: validaciju bih radio npr. kroz JSON Scheme, ali nisam htio
    # koristiti vanjske biblioteke.
    """
    Validate the input data. Every row of the input data must be a list
    containing two strings.

    Args:
        data: Data to be validated

    Returns:
        True if the data is valid, False otherwise
    """
    for item in data:
        if not isinstance(item, list):
            return False
        if not len(item) == 2:
            return False
        if not isinstance(item[0], str):
            return False
        if not isinstance(item[1], str):
            return False
    return True


def _match_data(names_by_id: List[FileDataEntry],
                surnames_by_id: List[FileDataEntry]) -> List[MatchedData]:
    """
    Match names and surnames by finding the corresponding IDs.
    Args:
        names_by_id: Rows of (name, id)
        surnames_by_id: Rows of (surname, id)

    Returns:
        Sorted, matched entries
    """
    key_fn = lambda n: n.value_id  # Extension 1
    names_by_id = sorted(names_by_id, key=key_fn)  # Extension 1
    surnames_by_id = sorted(surnames_by_id, key=key_fn)  # Extension 1

    for name_and_id, surname_and_id in zip(names_by_id, surnames_by_id):
        if name_and_id.value_id == surname_and_id.value_id:
            yield MatchedData(name=name_and_id.value,
                              surname=surname_and_id.value,
                              value_id=name_and_id.value_id)


if __name__ == '__main__':
    sys.exit(main())
