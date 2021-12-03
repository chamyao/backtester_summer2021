# backtester_summer2021
Public repository for our independently designed/written summer 2021 backtester project, a package that can be used to backtest market trading strategies. Commodity_cointegration is a example implementation of a pair-trading strategy using symbols selected through Engle-Granger cointegration tests. Design notes attached. 
Authors: Cham Yao, Matt Malitz, Thomas Clark. 

**Backtester Package Use Overview:**
  - import backtester.py from the backtester_package directory
  - input price history by providing the file path to directory containing ticker histories (.csv), fucntion: backtester.import_price_history *history directories can be generated from Yahoo Finance by using download_directory function in utilities.py (parameters: file path for .csv containing ticker symbols, start date, end date) 
  - run test by calling backtester.test (parameters: strategy function *see strategy function outline, test name, start date, end date)
 
Basic performance statistics are returned from calls backtester.test: total return, sharpe ratio, daily returns (list), daily portfolio value (list). Additionally, the program will generate a .txt file in the /logs directory recording the date and contents of every action taken by the strategy function. These logs can be revisited to further interpolate information on the performance of a test.

**Commodity cointegration:**
Example of a project utilizing the backtester package. Strategy function follows a pair-trading scheme, using pairs selected from Engle-Granger cointegration tests (cointegration_test.py). 

- Strategy generated by pair_trading.get_pair_strategy (parameters: symbol1, symbol2, entry bound-in terms of standard deviations, exit bound-in terms of standard deviations, lookback_window, spread_window). Entry and exit bollinger bands are calculated using the spread, lookback window, and bound parameters. 

- The strategy increases its spread holding multiplier by a factor of one each time the entry band is crossed in the upward direction, and then converts this to a target quantity values for both symbols proportional to the spread. The multiplier is converted to zero each time the exit bound is crossed in a downward direction and the target quantity for both symbols is set to zero.

***Strategy function outline:**
Strategy function refers to the first parameter in backtester.test, which takes in a function. The implementation of these functions is up to the programmer, the only restrictions being that they do not take in any parameters and output a concatenated string describing actions to be taken by the backtester each time it is called. Actions can be chained successively in a single string and are punctuated ith a ! sign.
- A full outline of supported actions can be found in the design notes or the apply_string function in utilities.py (Example of an action: "TP;{'AAPL': .25, 'MSFT': .5}!" - open or close positions of AAPL and MSFT symbols as needed to reach a specific target percent of the total portfolio.) 
