from TimeCost import TimeCost

data = list()
with open('data.csv', 'r') as file:
    lis = [line.split(';') for line in file]
    for i in range(0, len(lis), 1):
        temp = TimeCost(lis[i], True)
        data.append(temp)

with open('data1.csv', 'w') as file:
    for key in data:
        file.write("{};{}\n".format(key.date.strftime('%m.%d.%Y %H:%M'), key.cost * 100))
    file.close()