import os
import pandas_datareader as pdr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

SPY = pdr.get_data_tiingo('SPY', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')
TLT = pdr.get_data_tiingo('TLT', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')
SPY.reset_index(inplace=True)
TLT.reset_index(inplace=True)

Close = pd.concat([SPY.adjClose, TLT.adjClose], axis = 1)
Close.index = SPY.date
Close.columns = ['SPY', 'TLT']

#計算股價之相關係數
corr_matrix = Close.pct_change().apply(lambda x: np.log(1+x)).corr()
print("--------------------corr_matrix--------------------")
print(corr_matrix)

#預期報酬率
expected_return = Close.resample('Y').last()[:-1].pct_change().mean()
print("------------------Expected Return------------------")
print(expected_return)

#計算標準差
standard_dev = Close.pct_change().apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(250))
print("-----------------Standard Deviation----------------")
print(standard_dev)

# 投組報酬率
port_ret = []

# 投組標準差
port_dev = []

# 投組比例
port_weights = []

# 投組商品數
assets_nums = 2

# 不同投組的數量，點越多代表組合越多種，圖畫出來就越密
port_nums = 2000

# 計算共變異數
cov_matrix = Close.pct_change().apply(lambda x: np.log(1+x)).cov()

# random兩千個不同比例的投組，算出報酬率跟標準差
for port in range(2000):
    # random比例
    weights = np.random.random(assets_nums)
    weights = weights/np.sum(weights)
    port_weights.append(weights)
    
    # 計算平均報酬
    returns = np.dot(weights, expected_return)
    port_ret.append(returns)
    
    # 計算標準差
    var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()
    sd = np.sqrt(var)
    ann_sd = sd*np.sqrt(250)
    port_dev.append(ann_sd)

# 將資料整合成一個dataframe
data = {'Returns': port_ret, 'Standard Dev.': port_dev}

# 標註每個row使用的投組比例是多少
for counter, symbol in enumerate(Close.columns.tolist()):
    data[symbol+' weight'] = [w[counter] for w in port_weights]
    
# 整理資料成表格
portfolios = pd.DataFrame(data)
print(portfolios)

plt.figure(figsize=(15,10))
plt.scatter(x = portfolios['Standard Dev.'], y = portfolios['Returns'])
plt.grid()
plt.xlabel("Standard Dev.", fontsize=20)
plt.ylabel("Expected Returns", fontsize=20)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()