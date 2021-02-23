import csv
import statistics
from datetime import datetime, timezone
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from TradeEmulator import TradeEmulator

buy_percent = 1.007
sell_percent = 1.002
section_size = 60

def getEma(a: float, p: float, lastEma: float):
    return a * p + (1 - a) * lastEma

def getMeanSquareDeviation(data: list):
    middle_value = 0
    k = 0
    sma = float()
    for i in range(0, 4):
        sma += data[i]
    sma = sma / 4
    lastEma = sma

    for i in range(4, len(data)):
        lastEma = getEma(0.33, data[i], lastEma)
        middle_value += lastEma
        k += 1
    return lastEma
    #
    # i = 0
    # k = 1 / len(data)
    # s = 0
    # for key in data:
    #     l = k + (i*i)
    #     middle_value += key * l
    #     s += l
    #     i += 1
    # middle_value = middle_value / s
    # return middle_value


#print(getMeanSquareDeviation([3, 2, 2, 1, 3, 5, 7, 8, 9]))



prev_data = list()
emulator = TradeEmulator()
max_pick_value = None

def costAccepted(cost : float, date):
    global prev_data, max_pick_value
    global emulator, buy_percent, sell_percent
    if len(prev_data) < section_size:
        prev_data.append(cost)
        return

    middle_value = getMeanSquareDeviation(prev_data)
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
        print("{} middle_value = {} last_value = {} cost = {} calc_percent = {} amount = {} count = {}".format(date, middle_value, prev_data[len(prev_data) - 1], cost, calc_percent_buy, emulator.amount, emulator.count_ac))
    elif calc_percent_sell and calc_percent_sell > sell_percent and emulator.canSell():
        emulator.sell()
        print("{} max_pick_value = {} last_value = {} cost = {} calc_percent = {} amount = {} count = {}".format(date, max_pick_value, prev_data[len(prev_data) - 1], cost,
                                                                                             calc_percent_sell, emulator.amount, emulator.count_ac))
        prev_data.clear()
        max_pick_value = None
    prev_data.append(cost)
    prev_data.pop(0)

    pass


emulator.setCostAcceptedFunc(costAccepted)

emulator.start()

print(emulator.amount)