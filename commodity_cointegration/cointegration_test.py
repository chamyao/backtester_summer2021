import os
import pandas
from statsmodels.tsa.stattools import coint


def import_price_history(directory):
    securities = {}

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        data = pandas.read_csv(f, delimiter=',')
        prices = data.Close.tolist()[1:]
        tail = os.path.split(filename)[1]
        symbol = tail.split(sep='.')[0]
        if len(prices) == 1511:
            securities[symbol] = prices
            global dates
            dates = data.Date.tolist()[1:]
    return securities


securities = import_price_history('List of commodity ETFs_history')
df = pandas.DataFrame(data=securities)
test_file = open('results', 'w')
test_file.write('Cointegration test: ' + dates[0] + ' to ' + dates[199] + '\n\n')

results = {}
completed = []
for symbol in securities:
    for other in securities:
        if symbol != other and other not in completed:
            s1 = securities[symbol][:200]
            s2 = securities[other][:200]
            a, b, c = coint(s1, s2)
            if (b < .2):
                results[symbol + ',' + other] = a, b
    completed.append(symbol)

sorted_values = sorted(list(zip(*results.values()))[0])
sorted_results = {}

for i in sorted_values:
    for k in results.keys():
        if results[k][0] == i:
            sorted_results[k] = results[k]
            symbol1, symbol2 = k.split(',')
            a, b = results[k]
            test_file.write(symbol1 + ' | ' + symbol2 + '   t-statistic: ' + str(a) + '    p-factor: ' + str(b) + '\n')
            break
