import requests
import pandas as pd
import datetime as dt
from io import StringIO

starttime = dt.datetime.now()

year = int(input("Please enter year:"))

season = int(input("Please enter season:"))

if year >= 1000:
        year -= 1911

he = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

print("=================綜合損益表=================")

#綜合損益表
url = "https://mops.twse.com.tw/mops/web/t163sb04"

print("Begin requesting...")

session = requests.session()

r = session.post(url, {'encodeURIComponent':1, 'step':1,'firstin':1,'off':1,'TYPEK':'sii','year':str(year),'season':str(season)}, headers = he)

r.encoding = r.apparent_encoding

re = pd.read_html(r.text, header=None)

print("End requesting.")

print("Begin selecting...")

for i in range(len(re)):
    print("===============This is the ",i,"th table===============")
    print(re[i])

#bank = re[10]

all = re[12]

#holding = re[13]

#insurance = re[14]

print("End selecting.")

npp = all[["公司代號","本期淨利（淨損）"]]

npp.columns = ['公司代號','本期淨利']

oi = all[["公司代號","營業收入"]]

eps = all[["公司代號","基本每股盈餘（元）"]]

eps.columns = ['公司代號','每股稅後淨額']

#all.to_csv("all.csv",encoding="utf_8_sig")

print("=================資產負債表=================")
#資產負債表
url = "https://mops.twse.com.tw/mops/web/t163sb05"

print("Begin requesting...")

session = requests.session()

r = session.post(url, {'encodeURIComponent':1, 'step':1,'firstin':1,'off':1,'TYPEK':'sii','year':str(year),'season':str(season)}, headers = he)

r.encoding = r.apparent_encoding

re = pd.read_html(r.text, header=None)

print("End requesting.")

print("Begin selecting...")

all = re[12]

try:
    ta = all[["公司代號","資產總額"]]

    eq = all[["公司代號","權益總額"]]

except:
    ta = all[["公司代號","資產總計"]]

    eq = all[["公司代號","權益總計"]]

print("End selecting.")

print("==========稅後純益==========")

print(npp)

print("==========營業收入==========")

print(oi)

print("==========每股稅後淨額==========")

print(eps)

print("==========總資產==========")

print(ta)

print("==========股東權益==========")

print(eq)

endtime = dt.datetime.now()        
print("Prosess time:",endtime-starttime) 