import sys


def main():
    # read file
    with open('in.txt', 'r') as in_file:
        in_file = [x.strip() if 'Mozilla/' not in x
                   # remove browser info (decluster)
                   else x[:x.index('Mozilla/') - 1].strip()
                   for x in in_file.readlines()]

    # time zone info is the same everywhere, remove it (decluster)
    in_file = [x.replace(' -0700]', ']') for x in in_file]
    in_file = [x[:x.index(' "Wget')] if ' "Wget' in x
               else x
               for x in in_file]

    # split into collection of "(IP, rest of data)"
    in_file = [x.split(' - - ') for x in in_file]

    # get all the unique ip addresses
    keys = set(x[0] for x in in_file)

    # create a dictionary with all the ips as keys
    data_by_ip = {key: [] for key in keys}

    # split data by ip and save into dictionary
    for line in in_file:
        ip, data = line
        data_by_ip[ip].append(data)

    # save all the ips into new files
    for ip in data_by_ip.keys():
        with open(f'ip_{ip}.txt', 'w') as out_file:
            for data_item in data_by_ip[ip]:
                out_file.write(f'{data_item}\n')


if __name__ == '__main__':
    sys.exit(main())
