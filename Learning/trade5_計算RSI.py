import os
import pandas as pd
import numpy as np
import pandas_datareader as pdr

d = int(input("Please input target day period : "))

# RSI函數
def RSI(Close, period = d):
    # 整理資料
    Chg = Close - Close.shift(1)
    
    Chg_pos = pd.Series(index = Chg.index, data = Chg[Chg>0])
    Chg_pos = Chg_pos.fillna(0)
    #將空缺填補為0
    
    Chg_neg = pd.Series(index = Chg.index, data =- Chg[Chg<0])
    Chg_neg = Chg_neg.fillna(0)
    #將空缺填補為0
    
    # 計算12日平均漲跌幅度
    up_mean = []
    down_mean = []
    
    for i in range(period+1, len(Chg_pos)+1):
        up_mean.append(np.mean(Chg_pos.values[i-period:i]))
        down_mean.append(np.mean(Chg_neg.values[i-period:i]))
    
    # 計算 RSI
    rsi = []
    for i in range(len(up_mean)):
        rsi.append( 100 * up_mean[i] / ( up_mean[i] + down_mean[i] ) )
    
    rsi_series = pd.Series(index = Close.index[period:], data = rsi)
    return rsi_series

SPY = pdr.get_data_tiingo('SPY', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')

SPY = SPY.reset_index(level=[0,1])

SPY.index = SPY['date']

SPY_adj = SPY.iloc[:,7:12]

SPY_adj.columns = ['Close','High','Low','Open','Volume']

# 整理資料
# 收盤價
Close = SPY_adj.Close

print(RSI(Close))

'''
# 日漲跌
Chg = Close - Close.shift(1)

# 上漲幅度
Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg>0])
#轉為序列

Chg_pos = Chg_pos.fillna(0)
#用0填補資料空缺

# 下跌幅度(取正值，所以要加負號)
Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg<0])
#轉為序列

Chg_neg = Chg_neg.fillna(0)
#用0填補資料空缺

# 計算12日平均漲跌幅度

up_mean_12 = []
down_mean_12 = []
for i in range(13,len(Chg_pos)+1):
    up_mean_12.append(np.mean(Chg_pos.values[i-12:i]))
    down_mean_12.append(np.mean(Chg_neg.values[i-12:i]))

# 計算 RSI12
rsi_12 = []
for i in range(len(up_mean_12)):
    rsi_12.append( 100 * up_mean_12[i] / ( up_mean_12[i] + down_mean_12[i] ) )
rsi_12_series = pd.Series(index = Close.index[12:], data = rsi_12)

print(rsi_12_series)
'''
