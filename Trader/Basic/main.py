import requests
import pandas as pd
import datetime as dt
from io import StringIO

starttime = dt.datetime.now()

def fun_data(year,season):
        
        if year >= 1000:
                year -= 1911
        
        he = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
        
        print("=================綜合損益表=================")
        
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

        print("=================資產負債表=================")

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
    
    for i in range(2013,2021):
        for j in range(1,5):
            a = str(i)
            b = str(j)
            list.append(a+"_S"+b)
    
    for i in range(2015,2021):
        for j in range(1,5):
            a = str(i)
            b = str(j)
            time.append(a+"_S"+b)
    
    x = 0

    for i in range(2013,2021):
        for j in range(1,5):
            print("===========Requesting for", i ,"-", j,"===========")
            list[x] = fun_data(i,j)
            x += 1

    for i in range(0,32):
        list[i] = list[i][list[i]['營業收入'] != "--"]
        list[i]['營業收入'] = list[i]['營業收入'].astype(float)
    '''
    for i in range(0,32):
        print(i)
        print(sum((list[i]["本期淨利"]/list[0]["權益總額"]>0.05) & (list[i]["本期淨利"]/list[i]["營業收入"]>0.05) & (list[i]["資產總額"]/list[i]["權益總額"]-1<1)))
    '''

    tradeable = []
    for i in range(0,32):
        a = (list[i]["本期淨利"]/list[0]["權益總額"]>0.05) & (list[i]["本期淨利"]/list[i]["營業收入"]>0.05) & (list[i]["資產總額"]/list[i]["權益總額"]-1<1)
        b = list[i].loc[a,"公司代號"]
        tradeable.append(b)
        tradeable[i] = set(tradeable[i].unique())

    for_trade = []
    for i in range(8,32):
        a = tradeable[i].intersection(tradeable[i-1],tradeable[i-2],tradeable[i-3],tradeable[i-4],tradeable[i-5],tradeable[i-6],tradeable[i-7],tradeable[i-8])
        for_trade.append(a)

    di = dict(zip(time, for_trade))

    return di

fin = basic()

print(fin.items())

endtime = dt.datetime.now()        
print("Prosess time:",endtime-starttime)
    
