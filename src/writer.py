import csv
import os


class Writer:
    def __init__(self, first_row=tuple(), filename='output.csv'):
        self.filename = filename
        self.first_row = first_row

    def write(self, data):
        if not os.path.exists(self.filename):
            self.create_file()
        with open(self.filename, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

    def create_file(self):
        with open(self.filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.first_row)


if __name__ == '__main__':
    writer = Writer(first_row=['name', 'age'], filename='test.csv')
    writer.write(['andrey', '19'])
    writer.write(['vasya', '20'])
