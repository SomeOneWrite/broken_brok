import csv
from datetime import datetime, timezone
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from TimeCost import TimeCost

startime = datetime.strptime("20210120|000000", '%Y%m%d|%H%M%S')
endtime = datetime.strptime("20220121|130000", '%Y%m%d|%H%M%S')

alert_precent = 104.0

computed_alert_precent = alert_precent / 10000
data = list()

with open('data.txt', 'r') as file:
    lis = [line.split(';') for line in file]
    for i in range(0, len(lis), 1):
        temp = TimeCost(lis[i], False)
        data.append(temp)
data = sorted(data)

def getBoundedContent(data: list, start: datetime, end: datetime):
    filtered_data = list()
    for key in data:
        if start < key.date < end:
            filtered_data.append(key)
    return filtered_data

filtered_data = getBoundedContent(data, startime, endtime)

def getMeanSquareDeviation(data: list):
    middle_value = 0
    min = data[0].cost
    max = data[0].cost
    for key in data:
        middle_value += key.cost
        if min > key.cost:
            min = key.cost
        if max < key.cost:
            max = key.cost

    middle_value = middle_value / len(data)
    return middle_value, max, min


middle_value, max, min = getMeanSquareDeviation(filtered_data)

print(
    "Количество={} среднее={} минимум={} каксимум={}".format(
        len(filtered_data), middle_value, min, max))


def sectionMeaserment(data: list, section_size=6):
    for section_i in range(0, len(data) - 1, section_size):
        last = section_i + section_size - 1
        if last > len(data):
            continue
        next = last + 1
        if next >= len(data) - section_size:
            next = last
        next_it = data[next]
        last_it = data[last]

        section_data = list()
        for i in range(section_i, section_i + section_size):
            section_data.append(data[i])
        # print(' ||| '.join([str(x) for x in section_data]))
        middle_value, max, min = getMeanSquareDeviation(section_data)
        if last_it.cost == next_it.cost:
            continue
        current_middle_value, current_max, current_min = getMeanSquareDeviation([last_it, next_it])

        if (current_middle_value / middle_value / 100) > computed_alert_precent:
            st = ' ; '.join([str(x) for x in section_data])

            print("{} \n{} || {}  percent={} val1={} val2={}".format(st, last_it, next_it,
                                                                (current_middle_value / middle_value / 100),
                                                                middle_value, current_middle_value))

sectionMeaserment(filtered_data)

def save(name='', fmt='png'):
    pwd = os.getcwd()
    print("{} {}".format(pwd, '{}.{}'.format(name, fmt)))
    plt.savefig('{}.{}'.format(name, fmt), dpi=500)


def show(data: list):
    import matplotlib.pyplot as plt
    plt.figure()
    list_x = list()
    list_y = list()
    for i in range(0, len(data), 2):
        key = data[i]
        if i + 1 >= len(data):
            continue
        next_key = data[i + 1]
        timestamp = key.date.replace(tzinfo=timezone.utc).timestamp()
        timestamp_next = next_key.date.replace(tzinfo=timezone.utc).timestamp()
        list_x.append(timestamp)
        list_y.append(key.cost)
    list_x = np.array(list_x)
    list_y = np.array(list_y)
    for i in range(0, len(list_x)):
        plt.plot(list_x, list_y)

    plt.grid(True)  # линии вспомогательной сетки

    save(name=r'C:\Users\Anonim\desktop\pic_2_1', fmt='png')

    plt.show()

# show(filtered_data)
