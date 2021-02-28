import os
import pandas as pd
import numpy as np
import pandas_datareader as pdr
import matplotlib.pyplot as plt
from matplotlib import gridspec

# RSI函數
def RSI(Close, period=12):
    # 整理資料
    import pandas as pd
    Chg = Close - Close.shift(1)
    Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg>0])
    Chg_pos = Chg_pos.fillna(0)
    Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg<0])
    Chg_neg = Chg_neg.fillna(0)
    # 計算12日平均漲跌幅度
    import numpy as np
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

# RSI策略函數
def RSI_Trading_Sig(RSI, upper = 80, lower = 20):
    import pandas as pd
    # 訊號標籤
    sig = []
    # 庫存標籤，只會是0或1，表示每次交易都是買進或賣出所有部位
    stock = 0
    # 偵測RSI訊號
    for i in range(len(RSI)):
        if RSI[i] > upper and stock == 1:
            stock -= 1
            sig.append(-1)
        elif RSI[i] < lower and stock == 0:
            stock += 1
            sig.append(1)
        else:
            sig.append(0)
    # 將格式轉成 time series
    rsi_sig = pd.Series(index = RSI.index, data = sig)
    return rsi_sig

# RSI回測函數
def RSI_backtest(RSI_Trading_Sig, Open_Price):
    # 每次買賣的報酬率
    rets = []
    # 是否仍有庫存
    stock = 0
    # 當次交易買入價格
    buy_price = 0
    # 當次交易賣出價格
    sell_price = 0
    # 每次買賣的報酬率
    for i in range(len(RSI_Trading_Sig)-1):
        if RSI_Trading_Sig[i] == 1:
            # 隔日開盤買入
            buy_price = Open_Price[RSI_Trading_Sig.index[i+1]]
            stock += 1
        elif RSI_Trading_Sig[i] == -1:
            # 隔日開盤賣出
            sell_price = Open_Price[RSI_Trading_Sig.index[i+1]]
            stock -= 1
            rets.append((sell_price-buy_price)/buy_price)
            buy_price = 0
            sell_price = 0
    # 如果最後手上有庫存，就用回測區間最後一天的開盤價賣掉
    if stock == 1 and buy_price != 0 and sell_price == 0:
        sell_price = Open_Price[-1]
        rets.append((sell_price-buy_price)/buy_price)
    # 總報酬率
    total_ret = 1
    for ret in rets:
        total_ret *= 1 + ret
    return total_ret


# 串接API取資料
SPY = pdr.get_data_tiingo('SPY', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')
SPY = SPY.reset_index(level=[0,1])
SPY.index = SPY['date']
SPY_adj = SPY.iloc[:,7:12]
SPY_adj.columns = ['Close','High','Low','Open','Volume']

# 篩選2019年開收盤價資料
Close2019 = SPY_adj.Close['2019']
Open2019 = SPY_adj.Open['2019']

# 參數最佳化 No1，所有參數皆可調整
max_total_ret, max_period, max_upper, max_lower = 0, 0, 0, 0

for period in range(6,25):
    #將日期跑一遍
    for upper in range(70,91):
        #將上限跑一遍
        for lower in range(10,31):
            #將下線跑一遍
            ret = RSI_backtest(RSI_Trading_Sig(RSI(Close2019, period), upper, lower), Open2019)
            #ROI計算
            if ret > max_total_ret:
                max_total_ret, max_period, max_upper, max_lower = ret, period, upper, lower
            #if目前ROI大於歷史最大，則目前取代歷史最大

# 將求出來的結果印出參數及圖看看

x = RSI(Close2019, max_period).index
y = RSI(Close2019, max_period).values

fig = plt.figure(figsize=(15,10))
# set height ratios for sublots
gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

# the fisrt subplot
ax0 = plt.subplot(gs[0])
# line0 = ax0.plot(x, y, color='r')
ax0.plot(RSI(Close2019, max_period))
ax0.axhline(y=max_upper, color='red')
ax0.axhline(y=max_lower, color='green')

#the second subplot
# shared axis X
ax1 = plt.subplot(gs[1], sharex = ax0)
rsi_sig = pd.Series(index = RSI(Close2019, max_period).index, data = list(RSI_Trading_Sig(RSI(Close2019, max_period), max_upper, max_lower).values))
ax1.plot(rsi_sig)

print('Total ROI:', str(round(100*(max_total_ret-1),2)),'%')
print('Index: Day Period:', str(period) ,'Upper bond:' , str(max_upper) , 'Lower bond:' , str(max_lower))
plt.show()