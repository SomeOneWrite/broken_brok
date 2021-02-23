from TimeCost import TimeCost

data = list()
with open('data.csv', 'r') as file:
    lis = [line.split(';') for line in file]
    for i in range(0, len(lis), 1):
        temp = TimeCost(lis[i], True)
        data.append(temp)
data.sort()
with open('data2.csv', 'w') as file:
    k = 1
    for key in data:
        file.write("{};{}\n".format(k, key.cost))
        k += 1
    file.close()