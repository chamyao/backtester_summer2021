import backtester_package.backtester as backtester
import pandas
import matplotlib.pyplot as plt


def bollinger_bands(series, window, std):
    avg = series.rolling(window).mean()
    dev = series.rolling(window).std()
    return avg + dev * std, avg - dev * std


def get_pair_strategy(symbol1, symbol2, entry_std, exit_std, lookback_window, spread_window, max_mult=float('inf')):
    price_history = backtester.price_history
    price1 = price_history[symbol1]
    price2 = price_history[symbol2]
    series1 = pandas.Series(price1)
    series2 = pandas.Series(price2)
    alpha = None
    spread = None
    entry_bands = None
    exit_bands = None
    holding = False
    direction = None

    alpha = 2.42  # mean1 / mean2
    spread = series1 - alpha * series2
    entry_bands = bollinger_bands(spread, lookback_window, entry_std)
    exit_bands = bollinger_bands(spread, lookback_window, exit_std)

    multiplier = 0

    def strategy():
        nonlocal alpha
        nonlocal spread
        nonlocal entry_bands
        nonlocal exit_bands
        nonlocal holding
        nonlocal direction
        nonlocal multiplier
        date = backtester.datetime
        if alpha is None:  # experiment with dynamic values
            index1 = series1.index.get_loc(date)
            index2 = series2.index.get_loc(date)
            mean1 = series1.iloc[index1 - spread_window: index1 + 1].mean()
            mean2 = series2.iloc[index2 - spread_window: index2 + 1].mean()
            alpha = 2.42  # mean1 / mean2
            spread = series1 - alpha * series2
            entry_bands = bollinger_bands(spread, lookback_window, entry_std)
            exit_bands = bollinger_bands(spread, lookback_window, exit_std)

        output = ""
        quantity = backtester.portfolio.value() / (price1[date] + alpha * price2[date])

        upper, lower = entry_bands
        if multiplier < max_mult:
            if spread[date] < lower[date]:
                multiplier += 1
                output = "O;{s1};L;{q1}!O;{s2};S;{q2}!". \
                    format(s1=symbol1, s2=symbol2, q1=str(quantity), q2=str(quantity * alpha))
                direction = 'low'
                print('long open ' + date)
                print('Spread: ' + str(spread[date]))
            elif spread[date] > upper[date]:
                multiplier += 1
                output = "O;{s1};S;{q1}!O;{s2};L;{q2}!". \
                    format(s1=symbol1, s2=symbol2, q1=str(quantity), q2=str(quantity * alpha))
                direction = 'high'
                print('short open ' + date)
                print('Spread: ' + str(spread[date]))

        if multiplier > 0:
            upper, lower = exit_bands
            if direction == 'low' and lower[date] < spread[date]:
                output = "TQ;{{'{s1}': 0.0, '{s2}': 0.0}}!".format(s1=symbol1, s2=symbol2)
                multiplier = 0
                print('long close ' + date)
                print('Spread: ' + str(spread[date]))

            elif direction == 'high' and spread[date] < upper[date]:
                output = "TQ;{{'{s1}': 0.0, '{s2}': 0.0}}!".format(s1=symbol1, s2=symbol2)
                multiplier = 0
                print('short close ' + date)
                print('Spread: ' + str(spread[date]))

        return output

    return strategy, spread, entry_bands, exit_bands
