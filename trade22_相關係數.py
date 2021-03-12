import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt


def s(x, Sa, Sb, corr):
    return math.sqrt( (x**2) * Sa**2 + ((1-x)**2) * Sb**2 + 2 * x * (1-x) * corr * Sa * Sb )
# params
corr_set = [-1, -0.5, 0, 0.5, 1]

# standard deviation set
std_dev = []

# calculate standard deviations
for corr in corr_set:
    std_dev.append(s(0.6, 0.1, 0.3, corr))
df = pd.DataFrame({'corr': corr_set, 'std_dev': std_dev}, columns = ['corr','std_dev'])


# 預期報酬計算公式
def exp_return(x):
    return(9*x+18*(1-x))

# 計算不同組合下的預期報酬
rets=list(map(exp_return,[x/100 for x in range(101)]))

# 轉成 dataframe
rets_df = pd.DataFrame(index=list(range(0, 101)), data=rets, columns=['expected return'])

# 畫圖
plt.figure(figsize=(15,10))
plt.plot(rets_df)
plt.ylim([8,19])
plt.xlabel("A(%)", fontsize=20)
plt.ylabel("Expected Investment ROI(%)", fontsize=20)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()

# 投組標準差資料集合
std_dev_sets = []

# 計算標準差
for corr in corr_set:
    std_dev = []
    for x in range(0,101):
        std_dev.append(s(x/100, 0.1, 0.3, corr))
    std_dev_sets.append(std_dev)

# 繪圖
plt.figure(figsize=(15,10))
plt.plot(std_dev_sets[0],rets,label='corr = -1')
plt.plot(std_dev_sets[1],rets,label='corr = -0.5')
plt.plot(std_dev_sets[2],rets,label='corr = 0')
plt.plot(std_dev_sets[3],rets,label='corr = 0.5')
plt.plot(std_dev_sets[4],rets,label='corr = 1')
plt.xlabel('投組標準差(%)', fontsize=20)
plt.ylabel('Expected Investment ROI(%)', fontsize=20)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(loc='upper left',prop={'size': 15})

plt.show()


