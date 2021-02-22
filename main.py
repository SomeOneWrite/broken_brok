import csv
from datetime import datetime
import os
from datetime import datetime
from math import sqrt

import matplotlib.pyplot as plt

from TimeCost import TimeCost

startime = datetime.strptime("20210120|000000", '%Y%m%d|%H%M%S')
endtime = datetime.strptime("20210121|130000", '%Y%m%d|%H%M%S')

data = list()

with open('data.csv', 'r') as file:
    lis = [line.split(';') for line in file]
    for i in range(0, len(lis), 1):
        temp = TimeCost(lis[i], True)
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

    sum = 0
    for key in data:
        sum = sum + pow(middle_value - key.cost, 2)

    sum = sum / len(data)
    return middle_value, middle_value, max, min


middle_value, sum, max, min = getMeanSquareDeviation(filtered_data)

print(
    "Количество={} Среднее квадратичное отклонение={} Корень среднего квадратичного отклонения={} минимум={} каксимум={}".format(
        len(filtered_data), sum, sqrt(sum), min, max))
print("3 Сигма = {}".format(sqrt(sum) * 3))
print("middle_value={}".format(middle_value))


def sectionMeaserment(data: list, section_size=5):
    for section_i in range(0, len(data) - 1, section_size):
        last = section_i + section_size - 1
        next = last + 1
        if next >= len(data):
            next = next - 1
        next_it = data[next]
        last_it = data[last]

        section_data = list()
        for i in range(section_i, section_i + section_size):
            section_data.append(data[i])
        # print(' ||| '.join([str(x) for x in section_data]))
        middle_value, sum, max, min = getMeanSquareDeviation(section_data)
        if last_it.cost == next_it.cost:
            continue
        current_middle_value, current_max, current_min = getMeanSquareDeviation([last_it, next_it])
        if current_sum == 0:
            current_sum = sum
        if sum == 0:
            sum = current_sum

        if (current_sum / sum / 100) > 0.01006:
            st = ' ||| '.join([str(x) for x in section_data])

            print("{} \n{} {} percent={}".format(st, last_it, next_it, (current_sum / sum / 100)))


sectionMeaserment(filtered_data)


def save(name='', fmt='png'):
    pwd = os.getcwd()
    print("{} {}".format(pwd, '{}.{}'.format(name, fmt)))
    plt.savefig('{}.{}'.format(name, fmt), dpi=500)


def show(data: list):
    import matplotlib.pyplot as plt

    fig = plt.figure()

    for key in data:
        plt.scatter(key.date, key.cost, 1)

    grid1 = plt.grid(True)  # линии вспомогательной сетки

    save(name=r'C:\Users\Anonim\desktop\pic_2_1', fmt='png')

    plt.show()


#show(filtered_data)
