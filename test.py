import pandas as pd
import numpy as np
import pandas_datareader.data as pdr
import datetime as dt
import backtrader as bt
import backtrader.feeds as btfeeds
import requests 
import time


starttime = dt.datetime.now()


#----------------------Data----------------------
#上市汽車
#url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=&industry_code=12&Page=1&chklike=Y"

#上市半導體
url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=&industry_code=24&Page=1&chklike=Y"

#上市鋼鐵
#url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=&industry_code=10&Page=1&chklike=Y"

#上市類股
#url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"

response = requests.get(url)
listed = pd.read_html(response.text)[0]
listed.columns = listed.iloc[0,:]
listed = listed[["有價證券代號","有價證券名稱","市場別","產業別","公開發行/上市(櫃)/發行日"]]
listed = listed.iloc[1:]

stock_1 = listed["有價證券代號"]
stock_num = stock_1.apply(lambda x: str(x) + ".TW")

stocklist =  stock_num.tolist()

#stocklist = ["2498.TW"]

#----------------------Strategy----------------------
class MyStrategy(bt.Strategy):

    def __init__(self):
        self.volume = self.datas[0].volume
        self.price = self.datas[0].close
        self.sig = 0

    def next(self):     
        if self.volume[0] < min(self.volume[-1],self.volume[-2],self.volume[-3],self.volume[-4], self.volume[-5]) and self.price[0] < 1.03*(self.price[-1]+self.price[-2]+self.price[-3]+self.price[-4]+self.price[-5])/5 and self.price[0] > 0.97*(self.price[-1]+self.price[-2]+self.price[-3]+self.price[-4]+self.price[-5])/5:
            #and self.price[0] < 1.05*(self.price[-1]+self.price[-2]+self.price[-3]+self.price[-4]+self.price[-5])/5 and self.price[0] > 0.95*(self.price[-1]+self.price[-2]+self.price[-3]+self.price[-4]+self.price[-5])/5
            self.buy()
        
        #first signal => pending
        if self.sig == 0 and self.volume[0] > 1.5*max(self.volume[-1],self.volume[-2],self.volume[-3],self.volume[-4],self.volume[-5]) and self.price[0] > max(self.price[-1],self.price[-2]):
            self.sig = 1
        
        #second signal appear => sell
        elif self.sig == 1 and self.volume[0] > 1.5*max(self.volume[-1],self.volume[-2],self.volume[-3],self.volume[-4],self.volume[-5]) and self.price[0] > max(self.price[-1],self.price[-2]):
            self.sell()
            self.sig = 0

#----------------------BackTrader----------------------
alpha = 0.05
rornlist = []
rorplist = []
rorlist = []
maxror = 0
minror = 0
rorp = 0
rorn = 0
meanror = 0
meanrorp = 0
meanrorn = 0
trimeanror = 0
trimeanrorp = 0
trimeanrorn = 0
maxrorticker = " "
minrorticker = " "
y1 = 2010
m1 = 1
d1 = 1
y2 = 2021
m2 = 4
d2 = 26
dtstartdate = dt.datetime(y1,m1,d1)
dtenddate = dt.datetime(y2,m2,d2)

for stock in stocklist: 
    try:    
        print(stock,"begin")
        cerebro = bt.Cerebro()                                #起始函式
        cerebro.addstrategy(MyStrategy)                       #放入策略
        cerebro.broker.setcash(1000)                          #設定起始資金
        cerebro.broker.setcommission(commission=0.001)        #設定傭金

        #for dataname in stocklist:
        data = btfeeds.YahooFinanceData(dataname=stock, 
                                        fromdate=dtstartdate,
                                        todate=dtenddate)

        cerebro.adddata(data)                                 #放入股價資料
        #print("stock number:",dataname)
        
        inicash = cerebro.broker.getvalue()
        
        #print('Starting Value: %.2f' % inicash)
        cerebro.run()                                         #模擬交易結果
        
        endcash = cerebro.broker.getvalue()
        ror = (endcash/inicash -1)*100
        profit = endcash-inicash
        
        rorlist.append(ror)

        if ror > maxror:
            maxror = ror
            maxrorticker = stock
            print("max ror is:", maxror, "%, which is:", maxrorticker)
        
        if ror < minror:
            minror = ror
            minrorticker = stock
            print("min ror is:", minror, "%, which is:", minrorticker)

        if ror > 0:
            rorplist.append(ror)
        else: 
            rornlist.append(ror)

        print(stock,"end")
    
    except:
        print("Data Lost:",stock)


priceopen = [8644,4717,5575,4460,5907,6166,6457,7871,
8491,4725,8222,9039,7071,7738,8618,9292,8315,9252,10664,9725,12026,14720]
priceclose = [4739,5551,4452,5890,6139,6548,7823,8506,4591,8188,8972,7072,
7699,8611,9307,8338,9253,10642,9727,11997,14732,17572]

rorTaiex = (priceopen[y2-2000]/priceopen[y1-2000]-1)*100

rorlist.sort()
rorplist.sort()
rorplist.sort()

count = len(rorlist)
countp = len(rorplist)
countn = len(rornlist)

meanror = sum(rorlist)/len(rorlist)
meanrorp = sum(rorplist)/len(rorplist)
meanrorn = sum(rornlist)/len(rornlist)

del rorlist[0:int(alpha*len(rorlist))]
for i in range(int(alpha*len(rorlist))):
    rorlist.pop()

del rorplist[0:int(alpha*len(rorplist))]
for i in range(int(alpha*len(rorplist))):
    rorplist.pop()

del rornlist[0:int(alpha*len(rornlist))]
for i in range(int(alpha*len(rornlist))):
    rornlist.pop()

trimeanror = sum(rorlist)/len(rorlist)
trimeanrorp = sum(rorplist)/len(rorplist)
trimeanrorn = sum(rornlist)/len(rornlist)

print("__________________result__________________")
print("From:",dtstartdate,"To:",dtenddate)
print("Total number:",count)
print("Mean of ror is:",meanror,"%")
print("Ror of Taiex in same period:",rorTaiex)
if rorTaiex < meanror:
    print("This strategy is good, with ror:",meanror," >  ",
    rorTaiex,", which is ror of Taiex in same period.")
else :
    print("This startygy is not that good,with ror:",meanror," <  ",
    rorTaiex,", which is ror of Taiex in same period.")
print(alpha," trimean of ror is:",trimeanror,"%")
print("Number of positive ror:",countp)
print("Number of negetive ror:",countn)
print("Mean of positive ror:",meanrorp,"%")
print("Mean of negatove ror:",meanrorn,"%")
print(alpha," trimean of positive ror:",trimeanrorp,"%")
print(alpha," trimean of negatove ror:",trimeanrorn,"%")
print("Max ror is:", maxror,"%, which is:", maxrorticker)   
print("Min ror is:", minror,"%, which is:", minrorticker)

endtime = dt.datetime.now()        
print("Prosess time:",endtime-starttime)        

#cerebro.plot()
