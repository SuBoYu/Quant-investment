import os
from time import process_time
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt

SPY = pdr.get_data_tiingo('SPY', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')
TLT = pdr.get_data_tiingo('TLT', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')
GLD = pdr.get_data_tiingo('GLD', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')

SPY.reset_index(inplace=True)
TLT.reset_index(inplace=True)
GLD.reset_index(inplace=True)

Close = pd.concat([SPY.adjClose, TLT.adjClose, GLD.adjClose], axis = 1)
Close.index = SPY.date
Close.columns = ['SPY', 'TLT', 'GLD']

cov_matrix = Close.pct_change().apply(lambda x: np.log(1+x)).cov()
expected_return = Close.resample('Y').last()[:-1].pct_change().mean()
standard_dev = Close.pct_change().apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(250))
return_dev_matrix = pd.concat([expected_return, standard_dev], axis = 1)
return_dev_matrix.columns = ['Exp Returns', 'Standard Dev.']


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
# 無風險資產
plt.scatter(x = 0, y = 0.007, c = 'g', s = 100)
plt.annotate("100% U.S. CGB", (0,0.007), textcoords="offset points", xytext=(0,10), ha='left', fontsize=20)
# 繪圖設定
plt.grid()
plt.xlabel("Standard Dev.", fontsize=20)
plt.ylabel("Expected Returns", fontsize=20)
plt.xlim(-0.002,0.19)
plt.ylim(0,0.16)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()

# 找夏普比率最大的投組
max_sharpe = 0
max_sharpe_returns = 0
max_sharpe_std = 0
for i in range(len(eff_front_set)):
    sharpe = ( eff_front_set.iloc[i,:]['Returns'] - 0.007 ) / eff_front_set.iloc[i,:]['Standard Dev.']
    if sharpe > max_sharpe:
        max_sharpe = sharpe
        max_sharpe_std = eff_front_set.iloc[i,:]['Standard Dev.']
        max_sharpe_returns = eff_front_set.iloc[i,:]['Returns']
        max_sharpe_set = (eff_front_set.iloc[i,:]['SPY weight'], eff_front_set.iloc[i,:]['TLT weight'], eff_front_set.iloc[i,:]['GLD weight'])
print("ROI and Varience of sharpe raio", "(Returns, Standard Dev.) =", (max_sharpe_returns, max_sharpe_std))
print("Max sharpe raio conbination", "(SPY weight, TLT weight, GLD weight) =", max_sharpe_set)

plt.figure(figsize=(15,10))
# 效率前緣點，用紅色標註
plt.scatter(x = eff_front_std, y = eff_front_ret, c = 'r', s = 0.5)
# 無風險資產
plt.scatter(x = 0, y = 0.007, c = 'g', s = 100)
plt.annotate("100% U.S. CGB", (0,0.007), textcoords="offset points", xytext=(0,10), ha='left', fontsize=20)
# max sharpe set
plt.scatter(x = max_sharpe_std, y = max_sharpe_returns, c = 'orange', s = 100)
plt.annotate("Max sharpe raio conbination", (max_sharpe_std, max_sharpe_returns), textcoords="offset points", xytext=(15,-10), ha='left', fontsize=20)
# 切線
plt.plot([0,max_sharpe_std],[0.007, max_sharpe_returns])
# 繪圖設定
plt.grid()
plt.xlabel("Standard Dev.", fontsize=20)
plt.ylabel("Expected Returns", fontsize=20)
plt.xlim(-0.002,0.19)
plt.ylim(0,0.16)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()
