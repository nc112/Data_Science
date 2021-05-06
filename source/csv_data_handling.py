import csv

const_path = 'data/test_data_chinabank.csv'
const_encoding = ('GB2312', 'ASCII')


def read_csv_data(filename):
    with open(filename, 'r', encoding=const_encoding[0]) as csv_file:
        loaded_csv = csv.reader(csv_file)
        line_number = 0
        for line in loaded_csv:
            line_number += 1
            for element in line:
                if element == '':
                    print(type(line), ' ', line_number, element)


def missing_line_calculation(csv_data):
    assert type(csv_data) == list
    for line in csv_data:
        pass


if __name__ == '__main__':
    read_csv_data(const_path)
