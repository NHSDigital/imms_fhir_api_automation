import csv

def readInputCSV_search():
    with open('input_csv_files/searchParams.csv') as searchCSV:
        searchReader = csv.reader(searchCSV,delimiter=',')

        for row in searchReader:
            print(row)


