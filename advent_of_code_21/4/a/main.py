import sys


def main():
    with open('input.txt', 'r') as file:
        data = file.read().splitlines()

    data = [[int(x)
             for x in row.replace(',', ' ').split(' ')
             if x]
            for row in data
            if row]
    drawn_numbers = data[0]
    data = data[1:]
    tickets = [data[index: index + 5] for index in range(0, len(data), 5)]
    updated_tickets = tickets[:]

    for number in drawn_numbers:
        tickets = updated_tickets
        for ticket_number, ticket in enumerate(tickets):
            for row_number, row in enumerate(ticket):

                number_found_index_list = [index
                                           for index, row_element in
                                           enumerate(row)
                                           if row_element == number]
                for no in number_found_index_list:
                    updated_tickets[ticket_number][row_number][no] = 'x'

        for ticket_number, ticket in enumerate(updated_tickets):
            for row_number, row in enumerate(ticket):
                if len(set(row)) == 1 and set(row) == {'x'}:
                    print(number * sum([sum([x for x in row if x != 'x'])
                                        for row in ticket]))
                    return

            for pos in range(len(ticket[0])):
                column = [row[0] for row in ticket]
                if len(set(column)) == 1 and set(column) == {'x'}:
                    print(number * sum([sum([x for x in row if x != 'x'])
                                        for row in ticket]))
                    return


if __name__ == '__main__':
    sys.exit(main())
