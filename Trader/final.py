import requests
import pandas as pd
import datetime as dt
from io import StringIO
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas_datareader.data as pdr 

starttime = dt.datetime.now()

#----------------------Data----------------------

def fun_data(year,season):
        
        if year >= 1000:
                year -= 1911
        
        he = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
        
        print("==================綜合損益表==================")
        
        #綜合損益表
        url = "https://mops.twse.com.tw/mops/web/t163sb04"

        print("Begin requesting...")
        
        session = requests.session()

        r = session.post(url, {'encodeURIComponent':1, 'step':1,'firstin':1,'off':1,'TYPEK':'sii','year':str(year),'season':str(season)},headers = he)

        r.encoding = r.apparent_encoding

        re = pd.read_html(r.text, header=None)

        print("End requesting.")

        print("Begin selecting...")
        
        all = re[12]

        npp = all[["公司代號","本期淨利（淨損）"]]

        npp.columns = ['公司代號','本期淨利']

        oi = all[["營業收入"]]
        
        print("End selecting.")

        print("==================資產負債表==================")

        #資產負債表
        url = "https://mops.twse.com.tw/mops/web/t163sb05"

        print("Begin requesting...")

        session = requests.session()

        r = session.post(url, {'encodeURIComponent':1, 'step':1,'firstin':1,'off':1,'TYPEK':'sii','year':str(year),'season':str(season)},headers = he)

        r.encoding = r.apparent_encoding

        re = pd.read_html(r.text, header=None)

        print("End requesting.")

        print("Begin selecting...")

        all = re[12]

        try:
                ta = all[["資產總額"]]

                eq = all[["權益總額"]]

        except:
                ta = all[["資產總計"]]
                ta.columns = ['資產總額']

                eq = all[["權益總計"]]
                eq.columns = ['權益總額']
        
        print("End selecting.")
        
        result = pd.concat([npp, oi, ta, eq], axis=1)
        return(result)

def basic():
    
    time = []
    list = []
    
    for j in range(1,5):
        a = str(2013)
        b = str(j)
        list.append(a+"_S"+b)
    '''
    for i in range(2015,2021):
        for j in range(1,5):
            a = str(i)
            b = str(j)
            time.append(a+"_S"+b)
    '''
    x = 0

    i = 2013
    for j in range(1,5):
        print("===========Requesting for", i ,"-", j,"===========")
        list[x] = fun_data(i,j)
        x += 1

    for i in range(0,4):
        list[i] = list[i][list[i]['營業收入'] != "--"]
        list[i]['營業收入'] = list[i]['營業收入'].astype(float)

    tradeable = []
    for i in range(0,4):
        a = (list[i]["本期淨利"]/list[0]["權益總額"]>0.02) & (list[i]["本期淨利"]/list[i]["營業收入"]>0.05) & (list[i]["資產總額"]/list[i]["權益總額"]-1<1.5)
        b = list[i].loc[a,"公司代號"]
        tradeable.append(b)
        tradeable[i] = set(tradeable[i].unique())

    for_trade = []
    
    a = tradeable[3].intersection(tradeable[2],tradeable[1],tradeable[0])
    for_trade.append(a)

    set_1 = for_trade[0]
    '''
    for i in range(1,5):
        set_1 = set_1.union(for_trade[i])
    '''
    #di = dict(zip(time, for_trade))

    return set_1

fin = basic()

stock_1 = []
stocklist = []

stock_1 = list(fin)

stock_1.sort()

print("==========There're ",len(stock_1)," stocks to run.==========")

for i in range(len(stock_1)):
    stocklist.append(str(stock_1[i]) + ".TW")     
#----------------------Strategy----------------------
class MyStrategy(bt.Strategy):

    def __init__(self):
        self.volume = self.datas[0].volume
        self.price = self.datas[0].close
        self.sig = 0

    def next(self):     
        if self.volume[0] < min(self.volume[-1],self.volume[-2],self.volume[-3],self.volume[-4], self.volume[-5]) and self.price[0] < 1.03*(self.price[-1]+self.price[-2]+self.price[-3]+self.price[-4]+self.price[-5])/5 and self.price[0] > 0.97*(self.price[-1]+self.price[-2]+self.price[-3]+self.price[-4]+self.price[-5])/5:
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
y1 = 2014
m1 = 1
d1 = 1
y2 = 2021
m2 = 6
d2 = 15
dtstartdate = dt.datetime(y1,m1,d1)
dtenddate = dt.datetime(y2,m2,d2)

for stock in stocklist: 
    try:    
        print(stock,"begin")
        cerebro = bt.Cerebro()                                #起始函式
        cerebro.addstrategy(MyStrategy)                       #放入策略
        cerebro.broker.setcash(1000)                          #設定起始資金
        cerebro.broker.setcommission(commission=0.003)        #設定傭金

        #for dataname in stocklist:
        data = btfeeds.YahooFinanceData(dataname=stock, 
                                        fromdate=dtstartdate,
                                        todate=dtenddate)

        cerebro.adddata(data)                                 #放入股價資料
        
        inicash = cerebro.broker.getvalue()
        
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
7699,8611,9307,8338,9253,10642,9727,11997,14732,17213]

rorTaiex = (priceopen[y2-2000]/priceopen[y1-2000]-1)*100

count = len(rorlist)
meanror = sum(rorlist)/len(rorlist)

rorlist.sort()
rorplist.sort()
rorplist.sort()

countp = len(rorplist)
countn = len(rornlist)

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
print("Ror of Taiex in same period:",rorTaiex,"%")
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

