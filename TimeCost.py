from datetime import datetime


class TimeCost:

    def __init__(self, data : list, format = 1):
        self.format = format
        if format == 1:
            self.date = datetime.strptime("{}".format(data[0]), '%m.%d.%Y %H:%M') # 01.12.20 0:03
            self.cost = float(data[1])
        elif format == 2:
            self.date = datetime.strptime("{}|{}".format(data[2], data[3]), '%Y%m%d|%H%M%S')
            self.cost = float(data[4])
        elif format == 3:
            self.num = int(data[0])
            self.cost = float(data[1])

    def __lt__(self, other):
        if self.format > 2:
            return self.num < self.num
        return self.date < other.date

    def __str__(self):
        return "{} - {}".format(self.date, self.cost)


