import pandas as pd
import numpy as np
import urllib
import urllib.request
import requests as re
from bs4 import BeautifulSoup
import yfinance as yf
from pytrends.request import TrendReq
import datetime as dt
import time
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

import requests
import pandas as pd

url = 'https://www.slickcharts.com/sp500'
headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

request = requests.get(url, headers=headers)

data = pd.read_html(request.text)[0]

stk_list = data["Symbol"]

stk_list = data["Symbol"].apply(lambda x: x.replace(".", "-"))[:30]

# 上傳googleworksheet

# 基本認證流程
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('my-information-center-306014-e965617533fa.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open('investbook')

# 把 stk_info_df 所有股票基本資料，上傳到倉庫1 -stock_info
ws = sh.worksheet("investbook")

# 選擇要上傳的 cell，設定上傳內容
update_cell = 'C5'
k = ''
for i in range(len(stk_list) - 1):
    k += stk_list[i] + ', '
k += stk_list[len(stk_list) - 1]

print(k)
update_content = k

# 上傳
ws.update_acell(update_cell, update_content)

# 公司基本資料與價量資料
stock = yf.Ticker("AAPL")
stk_basic_data = stock.info
info_columns = list(stk_basic_data.keys())
# stk_info_df 存放所有股票基本資料
stk_info_df = pd.DataFrame(index=stk_list.sort_values(), columns=info_columns)
# stk_price_df 存放所有股票的價量資料
stk_price_df = pd.DataFrame(columns=["label", "Open", "High", "Low", "Close", "Adj Close", "Volume"])

cnt = 1
for i in stk_list:
    print("processing: " + i)
    print("cnt: ", cnt)
    cnt += 1
    stock = yf.Ticker(i)
    info_dict = stock.info
    columns_included = list(info_dict.keys())
    stk_info_df.loc[i, columns_included] = list(info_dict.values())
    temp = yf.download(i, start=dt.datetime.today() + dt.timedelta(-200))
    temp["label"] = i
    temp = temp.iloc[-90:, :]
    stk_price_df = stk_price_df.append(temp)
    time.sleep(1)

# 示範頁呈現的股票基本資料包含：股票名稱 / 最後報酬率 / 盤前報酬率 / 盤後報酬率 / 最後收盤價 / 盤前股價 / 盤後股價 / 最近一交易日股價區間 / 近一年股價區間
### 這邊基本資料爬下來會不太一樣，我們可以自己決定要放什麼資料


try:
    stk_info_df = stk_info_df[['longName', 'postMarketChangePercent', 'regularMarketPrice', 'postMarketPrice']]
except:
    stk_info_df = stk_info_df[['longName', 'regularMarketPrice']]

stk_price_df['Date'] = list(map(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'), list(stk_price_df.index)))
stk_price_df = stk_price_df[['label', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

print(stk_info_df)
print(stk_price_df)

# 上傳googleworksheet

#基本認證流程
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('my-information-center-306014-e965617533fa.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open('investbook')

# 把 stk_info_df 所有股票基本資料，上傳到倉庫1 -stock_info
ws = sh.worksheet("stock_info")
set_with_dataframe(ws, stk_info_df, row=1, col=1, include_index=True, include_column_header=True)

# 把 stk_price_df 所有股票價量資料，上傳到倉庫2 -stock_price
ws = sh.worksheet("stock_price")
set_with_dataframe(ws, stk_price_df, row=1, col=1, include_index=False, include_column_header=True)

# Google 最近90天搜尋量資料 100是最高
pytrends = TrendReq(hl = 'en-US', tz = 360)

# trend_df 將存放所有股票的 Google搜尋指數資料
trend_df = pd.DataFrame(columns = stk_list)
cnt = 1

for stk in stk_list:
    try:
        print("processing: " + stk)
        print("cnt: ", cnt)
        cnt += 1
        kw_list = [stk]
        pytrends.build_payload(kw_list, timeframe = "today 3-m")
        trend_df[stk] = pytrends.interest_over_time()[stk]
        time.sleep(1)
    except:
        continue

trend_df.index = list(map(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'), list(trend_df.index)))

print(trend_df)

# 上傳googleworksheet

#基本認證流程
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('my-information-center-306014-e965617533fa.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open('investbook')

# 把 stk_info_df 所有股票基本資料，上傳到倉庫1 -stock_info
ws = sh.worksheet("google_hot")
set_with_dataframe(ws, trend_df, row=1, col=1, include_index=True, include_column_header=True)

# 投資大師持股
# 由於每一檔股票，投資大師的數量都不一，因此先創一個空的 result 容器，後續迴圈的過程中，再把資料逐筆用 append 的方式紀錄
result = []
cnt = 1

for j in stk_list:
    try:
        # 針對 BRK-B 這檔股票，Gurufocus 網站的代碼辨認是 BRK.B
        if j == "BRK-B":
            j = "BRK.B"
        print("processing: " + j)
        print("cnt: ", cnt)
        cnt += 1
        soup = BeautifulSoup(re.get("https://www.gurufocus.com/stock/" + j + "/guru-trades").text, "html5lib")
        # 想爬的表格序號為 4，尋找所有 tr 標籤
        #         print(soup.find_all("table"))
        #         print("****************************")
        #         print(soup.find_all("table")[4])
        #         break
        for i in range(1, len(soup.find_all("table")[4].find_all("tr"))):
            # 每一筆資料都用 dictionary 紀錄
            data = {"stk": None,
                    "investor": None,
                    "port_date": None,
                    "current_share": None,
                    "per_outstand": None,
                    "per_total_asset": None,
                    "comment": None}

            data['stk'] = j
            data['investor'] = soup.find_all('table')[4].find_all('tr')[i].find_all('td')[0].get_text().replace('\n',
                                                                                                                '')
            data['port_date'] = soup.find_all('table')[4].find_all('tr')[i].find_all('td')[1].get_text()
            data['current_share'] = soup.find_all('table')[4].find_all('tr')[i].find_all('td')[2].get_text()
            data['per_outstand'] = soup.find_all('table')[4].find_all('tr')[i].find_all('td')[3].get_text()
            data['per_total_asset'] = soup.find_all('table')[4].find_all('tr')[i].find_all('td')[4].get_text()
            data['comment'] = soup.find_all('table')[4].find_all('tr')[i].find_all('td')[5].get_text()
            # print(data)
            # 填滿這筆紀錄的所有內容後，append 到 result 容器中
            result.append(data)

    except:
        print(j)
        continue

# print(result)
# 使用 pandas 的 .from_dict 將 dictionary 轉換為 DataFrame
big_trader_df = pd.DataFrame.from_dict(result)
big_trader_df = big_trader_df[list(big_trader_df.columns)[-1:] + list(big_trader_df.columns)[:-1]]

print(big_trader_df)

# 上傳googleworksheet

#基本認證流程
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('my-information-center-306014-e965617533fa.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open('investbook')

# 把 stk_info_df 所有股票基本資料，上傳到倉庫1 -stock_info
ws = sh.worksheet("big_traders")
set_with_dataframe(ws, big_trader_df, row=1, col=1, include_index=False, include_column_header=True)

# 重大經濟事件
# 類似於上一段的爬蟲方式

url = 'https://hk.investing.com/economic-calendar/'
r = urllib.request.Request(url)
r.add_header('User-Agent',
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')
response = urllib.request.urlopen(r)
soup = BeautifulSoup(response.read(), 'html.parser')

# 從 html 編碼中找出目標表格！
table = soup.find('table', {'id': 'economicCalendarData'})
content = table.find('tbody').findAll('tr', {'class': 'js-event-item'})

# 如同爬取投資大師持股資料的作法將資料紀錄在 dictionary，然後 append 在 result
result = []
for i in content:
    news = {'time': None,
            'country': None,
            'impact': None,
            'event': None,
            'actual': None,
            'forecast': None,
            'previous': None}

    news['time'] = i.attrs['data-event-datetime']
    news['country'] = i.find('td', {'class': 'flagCur'}).find('span').get('title')
    news['impact'] = i.find('td', {'class': 'sentiment'}).get('title')
    news['event'] = i.find('td', {'class': 'event'}).find('a').text.strip()
    news['actual'] = i.find('td', {'class': 'bold'}).text.strip()
    news['forecast'] = i.find('td', {'class': 'fore'}).text.strip()
    news['previous'] = i.find('td', {'class': 'prev'}).text.strip()
    result.append(news)

# 同樣地使用 .from_dict 將 result 轉換成 DataFrame
event_df = pd.DataFrame.from_dict(result)
event_df = event_df[list(event_df.columns)[-1:] + list(event_df.columns)[:-1]]

# 上傳googleworksheet

#基本認證流程
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('my-information-center-306014-e965617533fa.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open('investbook')

# 把 stk_info_df 所有股票基本資料，上傳到倉庫1 -stock_info
ws = sh.worksheet("global_event")
set_with_dataframe(ws, event_df, row=1, col=2, include_index=False, include_column_header=True)
