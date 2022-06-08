import sys


def main():
    # read file
    with open('journal.txt', 'r') as in_file:
        in_file = [x.strip() for x in in_file.readlines()]

    # remove everything but the file names
    in_file = [x[x.index('|') + 1:] for x in in_file]

    # find all created files
    print(f'CREATED {"=" * 100}')
    created_files = [x for x in in_file if 'CREATE' in x]
    # remove unnecessary data
    created_files = [x[:x.index('|')] for x in created_files]
    # remove duplicates but preserve order
    created_files = sorted(set([x for x in created_files]),
                           key=created_files.index)

    [print(x) for x in created_files]
    print(f'{"=" * 110}')

    # find all modified files
    print(f'MODIFIED {"=" * 100}')
    modified = [x[:x.index('|')] for x in in_file]
    # for readability, don't include created files in modified files
    modified = [x for x in modified if x not in created_files]
    # remove duplicates but preserve order
    modified = sorted(set([x for x in modified]), key=modified.index)
    [print(x) for x in modified]
    print(f'{"=" * 110}')


if __name__ == '__main__':
    sys.exit(main())
