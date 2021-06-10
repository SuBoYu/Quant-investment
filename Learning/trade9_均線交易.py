import pandas as pd
import talib
import matplotlib.pyplot as plt
import pandas_datareader as pdr

#基本資料引入，修改行名稱
SPY = pdr.get_data_tiingo('SPY', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')
SPY = SPY.reset_index(level=[0,1])
SPY.index = SPY['date']
SPY_adj = SPY.iloc[:,7:12]
SPY_adj.columns = ['Close','High','Low','Open','Volume']


# 取開盤價、收盤價
close = SPY_adj.Close
Open = SPY_adj.Open
Open2019 = Open['2019']

# 計算均線
ma5 = talib.SMA(close, timeperiod=5)
ma10 = talib.SMA(close, timeperiod=10)

# 繪圖
plt.figure(figsize=(15,10))
plt.plot(ma5['2019'])
plt.plot(ma10['2019'])
plt.legend(['5ma','10ma'])
plt.xticks(rotation='vertical')

#plt.show()

# 5ma與10ma差距
MA_dif = ma5 - ma10
#if MA_dif>0, then ma5 > ma10
MA_dif = MA_dif['2019']

# 參數
stock = 0
sig = [] 

# 訊號
for i in range(len(MA_dif)):
    # 5MA往上穿越10MA
    if MA_dif[i-1] < 0 and MA_dif[i] > 0 and stock == 0:
        # ma10 > ma5 ~ ma5 > ma10
        stock += 1
        sig.append(1)
    
    # 5MA往下穿越10MA
    elif MA_dif[i-1] > 0 and MA_dif[i] < 0 and stock == 1:
        #ma5 > ma10 ~ ma10 >ma5
        stock -= 1
        sig.append(-1)
    else:
        #無訊號
        sig.append(0)

#sig = 1 

# 製作dataframe
ma_sig = pd.Series(index = MA_dif.index, data = sig)
ma_sig_2019 = ma_sig['2019']

#回測

# 每次買賣的報酬率
rets = []
transaction = []

# 是否仍有庫存
stock = 0
stock_his = []

# 當次交易買入價格
buy_price = 0

# 當次交易賣出價格
sell_price = 0

# 每次買賣的報酬率
for i in range(len(ma_sig_2019)-1):
    stock_his.append(stock)
    
    #符合買入訊號
    if ma_sig_2019[i] == 1:
        
        #隔日開盤買入
        buy_price = Open2019[ma_sig_2019.index[i+1]]
        stock += 1
        #紀錄交易日期
        transaction.append([ma_sig_2019.index[i+1],'buy'])
    
    #符合賣出訊號
    elif ma_sig_2019[i] == -1:
        
        # 隔日開盤賣出
        sell_price = Open2019[ma_sig_2019.index[i+1]]
        stock -= 1
        rets.append((sell_price-buy_price)/buy_price)
        # 賣出後就清空資料
        buy_price = 0
        sell_price = 0
        # 紀錄交易日期
        transaction.append([ma_sig_2019.index[i+1],'sell'])

# 如果最後手上有庫存，就用回測區間最後一天的開盤價賣掉
if stock == 1 and buy_price != 0 and sell_price == 0:
    sell_price = Open2019[-1]
    rets.append((sell_price-buy_price)/buy_price)
    stock -= 1
    transaction.append([Open2019.index[-1],'sell'])

# 總報酬率
total_ret = 1

for ret in rets:
    total_ret *= 1 + ret

print('Total ROI：' + str(round(100*(total_ret-1),2)) + '%')

#印出交易日期
print(transaction)
