import numpy
import os
import talib
import pandas_datareader as pdr
# 看一下全部的函數，https://mrjbq7.github.io/ta-lib/funcs.html
all_functions = talib.get_functions()

#show all functions
print("Number of function:",len(all_functions))
print("--------------------------------------Functions--------------------------------------")
print(all_functions)

#show all groups
all_groups = talib.get_function_groups()
print("Number of group of function:",len(all_groups))
print("--------------------------------------Groups-----------------------------------------")
print(all_groups)

#基本資料引入，修改行名稱
SPY = pdr.get_data_tiingo('SPY', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')
SPY = SPY.reset_index(level=[0,1])
SPY.index = SPY['date']
SPY_adj = SPY.iloc[:,7:12]
SPY_adj.columns = ['Close','High','Low','Open','Volume']

MA5 = talib.SMA(SPY_adj.Close, timeperiod=5)
#計算五日均線
