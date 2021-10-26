import datetime
import pandas
import pandas_datareader as web
import os.path


def download(f_name, start, end):
    directory = f_name.split(sep='.')[0] + '_history'
    if not os.path.isdir(directory):
        os.mkdir(directory)

    f = open(f_name, 'r')
    data = pandas.read_csv(f, delimiter=',')
    symbols = data.Symbol.tolist()[1:]
    for symbol in symbols:
        file_name = directory + '/{}.csv'.format(symbol)
        try:
            data = web.DataReader(symbol, 'yahoo', start, end)
            f = open(file_name, 'w')
            f.write(data.to_csv())
        except:
            print(symbol + " error")


start = datetime.datetime(2015, 6, 3)
end = datetime.datetime(2021, 6, 3)

download('List of commodity ETFs.csv', start, end)


