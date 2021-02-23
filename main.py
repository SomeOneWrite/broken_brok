import csv
import statistics
from datetime import datetime, timezone
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from TradeEmulator import TradeEmulator

startime = datetime.strptime("20200112|000000", '%Y%m%d|%H%M%S')
endtime = datetime.strptime("20220121|130000", '%Y%m%d|%H%M%S')

buy_percent = 1.03
sell_percent = 1.01
section_size = 10



def getBoundedContent(data: list, start: datetime, end: datetime):
    filtered_data = list()
    for key in data:
        if start < key.date < end:
            filtered_data.append(key)
    return filtered_data

#filtered_data = getBoundedContent(data, startime, endtime)

def getMeanSquareDeviation(data: list):
    middle_value = 0
    min = data[0]
    max = data[0]
    for key in data:
        middle_value += key
        if min > key:
            min = key
        if max < key:
            max = key

    middle_value = statistics.median(data)
    return middle_value, max, min


prev_data = list()
emulator = TradeEmulator()
max_pick_value = None

def costAccepted(cost : float):
    global prev_data, max_pick_value
    global emulator, buy_percent, sell_percent
    if len(prev_data) <= section_size:
        prev_data.append(cost)
        return

    middle_value, max, min = getMeanSquareDeviation(prev_data)
    calc_percent_buy = (cost / middle_value)
    calc_percent_sell = None


    if emulator.canSell() and max_pick_value:
        if max_pick_value < cost:
            max_pick_value = cost
    if max_pick_value:
        calc_percent_sell = (max_pick_value / cost)
    if calc_percent_buy > buy_percent and emulator.canBuy():
        emulator.buy()
        max_pick_value = cost
        print("buy middle_value = {} cost = {} calc_percent = {} amount = {} count = {}".format(middle_value, cost, calc_percent_buy, emulator.amount, emulator.count_ac))
    elif calc_percent_sell and calc_percent_sell > sell_percent and emulator.canSell():
        emulator.sell()
        prev_data.clear()
        print("sell max_pick_value = {} cost = {} calc_percent = {} amount = {} count = {}".format(max_pick_value, cost,
                                                                                             calc_percent_sell, emulator.amount, emulator.count_ac))
        max_pick_value = None
    prev_data.append(cost)
    prev_data.pop(0)

    pass


emulator.setCostAcceptedFunc(costAccepted)

emulator.start()

print(emulator.amount)