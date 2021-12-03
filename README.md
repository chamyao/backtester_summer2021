# backtester_summer2021
Public repository for our summer 2021 backtester project. Commodity_cointegration is a example implementation of a pair-trading strategy using symbols selected through Engle-Granger cointegration tests. Design notes attached.
Authors: Cham Yao, Matt Malitz, Thomas Clark.

**Backtester Package Overview:**

_Use:_
  - import backtester.py from the backtester_package directory
  - input price history by providing the file path to directory containing ticker histories (.csv), fucntion: backtester.import_price_history *history directories can be generated from Yahoo Finance by using download_directory function in utilities.py (parameters: file path for .csv containing ticker symbols, start date, end date) 
  - run test by calling backtester.test (parameters: strategy function *see strategy function outline, test name, start date, end date)
 
Basic performance statistics are returned from calls backtester.test: total return, sharpe ratio, daily returns (list), daily portfolio value (list). Additionally, the program will generate a .txt file in the /logs directory recording the date and contents of every action taken by the strategy function. These logs can be revisited to further interpolate information on the performance of a test.
 
*Strategy outline*

Strategy function refers to the first parameter in backtester.test, which takes in a function. The implementation of these functions is up to the programmer, the only restrictions being that they do not take in any parameters and output a descriptive string detailing actions to be taken by the backtester each time it is called. A full outline of supported actions are outlined in the design notes and the apply_string function in utilities.py (Examples of actions include: open or close positions of a symbol as needed to reach a specific target percent of the total portfolio, open or close positions of a symbol by a specified amount, etc.) 
