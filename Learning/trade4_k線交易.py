import os
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt

def Evening_Star_Sig(data):
    # 開盤價/收盤價
    data_Open = data.Open
    data_Close = data.Close
    
    # 當日漲跌
    data_DailyChg = data_Close - data_Open
    
    # 取得每日的振幅
    data_Abs_DailyChg = abs(data_DailyChg)
    
    # 計算統計數據
    mean = data_Abs_DailyChg.mean()
    first_quar = data_Abs_DailyChg.quantile(q=0.25)
    
    # 抓取 第1根大振幅陽線、第2根小振幅陽線或陰線、第3根陰線且振幅大於第1根的1/2
    evening_condition_1 = [0,0]
    for i in range(2, len(data_DailyChg)):
        if ( data_DailyChg[i-2] > mean ) & ( abs(data_DailyChg[i-1]) < first_quar ) & ( data_DailyChg[i] < -0.5*mean ):
            evening_condition_1.append(1)
        else:
            evening_condition_1.append(0)
            
    # 第2根的開盤與收盤價 均大於 第1根的收盤與第3根的開盤
    evening_condition_2 = [0,0]
    for i in range(2, len(data_Open)):
        if ( data_Open[i-1] > data_Close[i-2] ) & ( data_Open[i-1] > data_Open[i] ) & ( data_Close[i-1] > data_Close[i-2] ) & ( data_Close[i-1] > data_Open[i] ):
            evening_condition_2.append(1)
        else:
            evening_condition_2.append(0)
            
    # Evening Star Signal
    evening_star_signal = []
    for i in range(len(evening_condition_1)):
        if ( evening_condition_1[i] == 1 ) & ( evening_condition_2[i] == 1 ):
            evening_star_signal.append(1)
        else:
            evening_star_signal.append(0)
            
    # Return a boolean series
    import pandas as pd
    sig = pd.Series(index = data.index, data = evening_star_signal)
    sig = sig.astype('bool')
    return sig

SPY = pdr.get_data_tiingo('SPY', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')

SPY = SPY.reset_index(level=[0,1])

SPY.index = SPY['date']

SPY_adj = SPY.iloc[:,7:11]

SPY_adj.columns = ['Close','High','Low','Open']

sig = Evening_Star_Sig(SPY_adj)
#sig唯一時間序列，若有符合條件則為true，反之為false

SPY_Open_adj = SPY_adj.Open
#定義出開盤價

ret1 = SPY_Open_adj.shift(-2) / SPY_Open_adj.shift(-1)
#可以用夜星做隔日冲的日期

ret5 = SPY_Open_adj.shift(-6) / SPY_Open_adj.shift(-1)
#可以用夜星做五日冲的日期

ret1riserate =  ret1[sig].mean()
#計算夜星隔日上漲率

ret5riserate =  ret5[sig].mean()
#計算夜星五日上漲率

# 回測 Evening star出現後，買賣間隔1~100天的平均報酬率
rets = []
for i in range(2,102):
    ret = SPY_Open_adj.shift(-i) / SPY_Open_adj.shift(-1)
    rets.append(ret[sig].mean())
#將隔日冲到百日冲的報酬率列出    
    
# 畫出天數對應報酬率的圖
ret_df = pd.DataFrame(index = range(1,101), data = rets)

ret_df.columns = ['return']

ret_df = (ret_df-1) * 100

plt.figure(figsize = (12,8))

plt.plot(ret_df)

plt.hlines(y = 0, xmin = 0, xmax = 100, color='red')

plt.title("Average Return Rate(%) v.s. Data Period(Days)",fontsize=15)
#設定圖表標題

plt.xlabel("Date Period(Days)", fontsize=15)
#設定x軸標題

plt.ylabel("Average Return Rate(%)", fontsize=15)
#設定y軸標題

plt.show()
#顯示圖表
