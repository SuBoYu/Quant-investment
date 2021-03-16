import os
from time import process_time
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt

#爬取資料
SPY = pdr.get_data_tiingo('SPY', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')
TLT = pdr.get_data_tiingo('TLT', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')
GLD = pdr.get_data_tiingo('GLD', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')

SPY.reset_index(inplace=True)
TLT.reset_index(inplace=True)
GLD.reset_index(inplace=True)

Close = pd.concat([SPY.adjClose, TLT.adjClose, GLD.adjClose], axis = 1)
Close.index = SPY.date
Close.columns = ['SPY', 'TLT', 'GLD']

#共變異數
cov_matrix = Close.pct_change().apply(lambda x: np.log(1+x)).cov()
print("--------------------Cov_Matrix--------------------")
print(cov_matrix)

#預期報酬                                                  
expected_return = Close.resample('Y').last()[:-1].pct_change().mean()
print("--------------------Expcted_Return--------------------")
print(expected_return)

#標準差                                                                                                                ㄝ
standard_dev = Close.pct_change().apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(250))
print("--------------------Standard_Dev--------------------")
print(standard_dev)

return_dev_matrix = pd.concat([expected_return, standard_dev], axis = 1)
return_dev_matrix.columns = ['Exp Returns', 'Standard Dev.']
print("--------------------Return_Dev_Matrix--------------------")
print(return_dev_matrix)

port_ret = []
port_dev = []
port_weights = []
assets_nums = 3
port_nums = 2000

for port in range(2000):
    weights = np.random.random(assets_nums)
    weights = weights/np.sum(weights)
    port_weights.append(weights)
    returns = np.dot(weights, expected_return)
    port_ret.append(returns)
    var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()
    sd = np.sqrt(var)
    ann_sd = sd*np.sqrt(250)
    port_dev.append(ann_sd)
    
data = {'Returns': port_ret, 'Standard Dev.': port_dev}

for counter, symbol in enumerate(Close.columns.tolist()):
    data[symbol+' weight'] = [w[counter] for w in port_weights]
    
portfolios = pd.DataFrame(data)
print(portfolios.head())

'''
#劃出配置圖表
plt.figure(figsize=(15,10))
plt.scatter(x = portfolios['Standard Dev.'], y = portfolios['Returns'])
plt.grid()
plt.xlabel("Standard Dev.", fontsize=20)
plt.ylabel("Expected Returns", fontsize=20)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
'''

# 取效率前緣
std = []
ret = [portfolios[portfolios['Standard Dev.'] == portfolios['Standard Dev.'].min()]['Returns'].values[0]]
eff_front_set = pd.DataFrame(columns=['Returns', 'Standard Dev.', 'SPY weight', 'TLT weight', 'GLD weight'])

for i in range(800,1800,1):
    df = portfolios[(portfolios['Standard Dev.'] >= i/10000) & (portfolios['Standard Dev.'] <= (i+15)/10000)]
    try:
        # 上側
        max_ret = df[df['Returns'] == df['Returns'].max()]['Returns'].values[0]
        if max_ret >= max(ret):
            std.append(df[df['Returns'] == df['Returns'].max()]['Standard Dev.'].values[0])
            ret.append(df[df['Returns'] == df['Returns'].max()]['Returns'].values[0])
            eff_front_set = eff_front_set.append(df[df['Returns'] == df['Returns'].max()], ignore_index = True)
    except:
        pass

ret.pop(0)
eff_front_std = pd.Series(std)
eff_front_ret = pd.Series(ret)

plt.figure(figsize=(15,10))
plt.scatter(x = portfolios['Standard Dev.'], y = portfolios['Returns'])

# 效率前緣點，用紅色標註
plt.scatter(x = eff_front_std, y = eff_front_ret, c = 'r')
plt.grid()
plt.xlabel("Standard Dev.", fontsize=20)
plt.ylabel("Expected Returns", fontsize=20)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()

#資產配置數據
print(eff_front_set)