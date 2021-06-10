import os
import pandas_datareader as pdr
import mplfinance as mpf

SPY = pdr.get_data_tiingo('SPY', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')
#利用API取得資料

SPY = SPY.reset_index(level=[0,1])
#將multi-index轉成single-index

SPY.index = SPY['date']
#指定date為index

SPY_adj = SPY.iloc[:,7:11]
#取adjClose至adjOpen的欄位資料

SPY_adj.columns = ['Close','High','Low','Open']
#更改columns的名稱，以讓mplfinance看得懂

SPY_adj_2019 = SPY_adj['2019']
#取2019年的數據

SPY_adj_2019_Open = SPY_adj_2019.Open
SPY_adj_2019_Close = SPY_adj_2019.Close
#開盤價 & 收盤價

SPY_DailyChg_2019 = SPY_adj_2019_Close - SPY_adj_2019_Open
#當日漲跌點數

SPY_Abs_DailyChg_2019 = abs(SPY_DailyChg_2019)
#取得每日的振幅(當日漲幅的絕對值)

#SPY_Abs_DailyChg_2019.describe()
#能夠輸出mean、std、min、max、25、50、75


# 抓取 第1根大振幅陽線、第2根小振幅陽線或陰線、第3根陰線且振幅大於第1根的1/2
evening_condition_1 = [0,0]
#一天一次、故重複資料長度

for i in range(2, len(SPY_DailyChg_2019)):
    if ( SPY_DailyChg_2019[i-2] > 1.158 ) & ( abs(SPY_DailyChg_2019[i-1]) < 0.388 ) & ( SPY_DailyChg_2019[i] < -0.58 ):
        #第一根大於平均長度                        第二根比25%小                           第三根超過第一個根的一半
        evening_condition_1.append(1)
        #若符合，標記為1
    else:
        evening_condition_1.append(0)
        #反之為0
        
evening_condition_1.count(1)
#condition 1 符合的次數

#第2根的開盤與收盤價 均大於 第1根的收盤與第3根的開盤
evening_condition_2 = [0,0]

for i in range(2, len(SPY_adj_2019_Open)):
    if ( SPY_adj_2019_Open[i-1] > SPY_adj_2019_Close[i-2] ) & ( SPY_adj_2019_Open[i-1] > SPY_adj_2019_Open[i] ) & ( SPY_adj_2019_Close[i-1] > SPY_adj_2019_Close[i-2] ) & ( SPY_adj_2019_Close[i-1] > SPY_adj_2019_Open[i] ):
         #第二根開盤大於第一根收盤                               第二根開盤大於第三根開盤                                第二根收盤大於第三根收盤                                     第二根收盤大於第三根開盤
        evening_condition_2.append(1)
        #若符合，標記為1
    else:
        evening_condition_2.append(0)
        #反之為0
        
evening_condition_2.count(1)

# Evening Star Signal
evening_star_signal = []

for i in range(len(evening_condition_1)):
    if ( evening_condition_1[i] == 1 ) & ( evening_condition_2[i] == 1 ):
        #兩個都符合
        evening_star_signal.append(1)
        #則標記為1
    else:
        evening_star_signal.append(0)
        #反之為0
        
# Find Evening Star date
for i in range(len(evening_star_signal)):
    if evening_star_signal[i] == 1:
        print(SPY_adj_2019.index[i])
        
SPY_adj_2019_Aug = SPY_adj_2019['2019-08']
#篩出2019_8的資料

mpf.plot(SPY_adj_2019_Aug,type='candle')
#匯出2019_8的K線圖
