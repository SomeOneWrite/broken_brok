from datetime import datetime


class TimeCost:

    def __init__(self, data : list, isCsv = False):
        if isCsv:
            self.date = datetime.strptime("{}".format(data[0]), '%m.%d.%Y %H:%M') # 01.12.20 0:03
            self.cost = float(data[1])
        else:
            self.date = datetime.strptime("{}|{}".format(data[2], data[3]), '%Y%m%d|%H%M%S')
            self.cost = float(data[4])

    def __lt__(self, other):
        char = ''
        if self.date < other.date:
            char = '<'
        else:
            char = '>'
       # print("{} {} {}".format(self.date, char, other.date))
        return self.date < other.date

    def __str__(self):
        return "{} || {}".format(self.date, self.cost)


