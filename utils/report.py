import csv


class ReportUtils:
    @staticmethod
    def read_widget_ids():
        widget_list = []
        file_path = 'assets/report/widget_list.csv'
        with open(file_path) as csvfile:
            data = csv.reader(csvfile)
            next(data)
            for row in data:
                widget_list.append(row[0])
        return widget_list
