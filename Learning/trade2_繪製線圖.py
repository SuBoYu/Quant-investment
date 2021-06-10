import os
import pandas_datareader as pdr
import mplfinance as mpf

GOOG = pdr.get_data_tiingo('GOOG', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')
#對接TIINGO，將GOOG存進df

GOOG = GOOG.reset_index(level=[0,1])
#將multi-index轉成single-index

GOOG.index = GOOG['date']
#指定date為index

GOOG_adj = GOOG.iloc[:,7:11]
#取adjClose至adjOpen的欄位資料

GOOG_adj.columns = ['Close','High','Low','Open']
#更改columns的名稱，以讓mplfinance看得懂

GOOG_adj_20d = GOOG_adj.iloc[-1000:,:]
#抓取近20日的資料

print(mpf.plot(GOOG_adj_20d))
#一般線圖

print(mpf.plot(GOOG_adj_20d,type = 'candle'))
#k線圖

print(mpf.plot(GOOG_adj_20d,type = 'line'))
#折線圖
