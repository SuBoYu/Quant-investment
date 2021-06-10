import os
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas_datareader as pdr

SPY = pdr.get_data_tiingo('SPY', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')
AAPL = pdr.get_data_tiingo('AAPL', api_key='d1ba1257b1cf49025b398277e33264e6a1a53cac')

# SPY 2019 日報酬率
SPY = SPY.reset_index(level=[0,1])
SPY.index = SPY['date']
SPY_adj = SPY.iloc[:,7:11]
SPY_adj.columns = ['Close','High','Low','Open']
SPY_Close_adj = SPY_adj.Close
ret1 = SPY_Close_adj.shift(-2) / SPY_Close_adj.shift(-1)
spy_daily_ret = ret1 - 1
spy_daily_ret_2019 = spy_daily_ret['2019']

# AAPL 2019 日報酬率
AAPL = AAPL.reset_index(level=[0,1])
AAPL.index = AAPL['date']
AAPL_adj = AAPL.iloc[:,7:11]
AAPL_adj.columns = ['Close','High','Low','Open']
AAPL_Close_adj = AAPL_adj.Close
ret1 = AAPL_Close_adj.shift(-2) / AAPL_Close_adj.shift(-1)
aapl_daily_ret = ret1 - 1
aapl_daily_ret_2019 = aapl_daily_ret['2019']

# 整合成一個dataframe
import pandas as pd
ret_data = pd.concat([aapl_daily_ret_2019,spy_daily_ret_2019], axis = 1)
ret_data.columns = ['AAPL', 'SPY']

# risk free return
rf_ret = 1.0078 ** ( 1 / 252 ) - 1

Ex_ret = ret_data - rf_ret

plt.rcParams['axes.unicode_minus']=False

plt.scatter(Ex_ret.values[:,0],Ex_ret.values[:,1])
plt.title('AAPL return and SPY return')

plt.show()

model=sm.OLS(Ex_ret.AAPL[1:],sm.add_constant(Ex_ret.SPY[1:]))
result=model.fit()
print(result.summary())



