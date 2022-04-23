import csv

from src.scraper.ColumnMapper import MapperClass


class readCSV:
    def getAllRows(self):
        with open('All_Jobs.csv', 'r') as file:
            reader = csv.DictReader(file)
            # rows = list(reader)
            jobList = []
            for row in reader:
                data = {}
                for header, value in row.items():
                        mapClass = MapperClass()
                        data[str(mapClass.columnMapper.get(header))]= str(value)
                jobList.append(data)
        return jobList


