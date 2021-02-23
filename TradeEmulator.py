from TimeCost import TimeCost


class TradeEmulator:
    def __init__(self):
        self.func = None
        self._parseData()
        self.amount = 1000
        self.current_cost = 0
        self.count_ac = 0
        pass

    def start(self):
        if self.func:
            for key in self.data:
                self.current_cost = key.cost
                self.func(key.cost)

    def _parseData(self):
        self.data = list()
        with open('data.csv', 'r') as file:
            lis = [line.split(';') for line in file]
            for i in range(0, len(lis), 1):
                temp = TimeCost(lis[i], 1)
                self.data.append(temp)
        self.data.sort()

    def setCostAcceptedFunc(self, func):
        self.func = func

    def buy(self):
        self.count_ac = self.amount // self.current_cost
        self.amount -= self.count_ac * self.current_cost
        print("buy amount={} count={}".format(self.amount, self.count_ac))
        pass

    def sell(self):
        self.amount += self.count_ac * self.current_cost
        self.count_ac = 0
        print("sell amount={}".format(self.amount))
        pass

    def canBuy(self):
        return (self.amount // self.current_cost) != 0

    def canSell(self):
        return self.count_ac != 0


