import os

import pandas as pd
import matplotlib.pyplot as plt


def bollinger_bands(series, window, std):
    avg = series.rolling(window).mean()
    dev = series.rolling(window).std()
    return avg + dev * std, avg - dev * std


def import_price_history(directory):
    securities = {}

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        data = pd.read_csv(f, delimiter=',')
        prices = data.Close.tolist()[1:]
        tail = os.path.split(filename)[1]
        symbol = tail.split(sep='.')[0]
        if len(prices) == 1511:
            securities[symbol] = prices
            global dates
            dates = data.Date.tolist()[1:]
    return securities


securities = import_price_history('List of commodity ETFs_history')
df = pd.DataFrame(data=securities)

# plt.plot(df.OIL)
# plt.plot(df.WEAT * df.OIL.mean() / df.WEAT.mean())
spread = df.OIL - df.WEAT * df.OIL.mean() / df.WEAT.mean()
std = spread.std()
plt.plot(spread)
upper, lower = bollinger_bands(spread, 100, 2)
upper_a, lower_a = bollinger_bands(spread, 100, .5)
# plt.plot(spread.rolling(100).mean())
plt.plot(upper)
plt.plot(lower)
plt.plot(upper_a)
plt.plot(lower_a)
plt.show()
