import datetime
import sys


def main():
    # read file
    with open('journal.txt', 'r') as in_file:
        in_file = [x.strip() for x in in_file.readlines()]

    # split data
    in_file = [x.split('|') for x in in_file]

    # get only date, name, modification info
    in_file = [(datetime.datetime.strptime(x[3][:-2], '%Y-%m-%d %H:%M:%S.%f'),
                x[1],
                x[4])
               for x in in_file]
    # correct time zone
    in_file = [(date - datetime.timedelta(hours=7), n, i)
               for date, n, i in in_file]
    # back to string
    in_file = [(date.isoformat().replace('T', ' '), n, i)
               for date, n, i in in_file]

    # find all created files
    print(f'CREATED {"=" * 100}')
    # format the output as "date - name"
    created_files = [f'{x[0]} - {x[1]}' for x in in_file if 'CREATE' in x[2]]
    # remove duplicates but preserve order
    created_files = sorted(set([x for x in created_files]),
                           key=created_files.index)
    [print(x) for x in created_files]
    print(f'{"=" * 110}')

    # find all modified files
    print(f'MODIFIED {"=" * 100}')
    modified = [f'{x[0]} - {x[1]}' for x in in_file]
    # for readability, don't include created files in modified files
    modified = [x for x in modified if x not in created_files]
    # remove duplicates but preserve order
    modified = sorted(set([x for x in modified]), key=modified.index)
    [print(x) for x in modified]
    print(f'{"=" * 110}')


if __name__ == '__main__':
    sys.exit(main())
