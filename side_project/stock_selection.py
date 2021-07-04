import time
import random
import requests
import pandas as pd
import datetime as dt
from io import StringIO
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas_datareader.data as pdr

starttime = dt.datetime.now()

#營收成長性
url = "https://mops.twse.com.tw/nas/t21/sii/t21sc03_103_2_0.html"
#月報https://www.finlab.tw/%E8%B6%85%E7%B0%A1%E5%96%AE%E7%94%A8python%E6%8A%93%E5%8F%96%E6%AF%8F%E6%9C%88%E7%87%9F%E6%94%B6/
#月營收月增率>0(5)
#月營收年增率>0(5)
#累計營收年增率>0(10)

#獲利成長性
import time
import random
import sqlite3
import requests
import pandas as pd
import datetime as dt

starttime = dt.datetime.now()

for year in range(102, 110):
    for season in range(1, 5):
        time.sleep(random.uniform(1, 5))

        he = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

        print("================This is ", year, "_", season, "================")

        print("====================營益分析表====================")

        # 營益分析表
        url = "https://mops.twse.com.tw/mops/web/t163sb06"

        print("Begin requesting...")

        session = requests.session()

        r = session.post(url,
                         {'encodeURIComponent': 1, 'step': 1, 'firstin': 1, 'off': 1, 'TYPEK': 'sii', 'year': str(year),
                          'season': str(season)}, headers=he)

        r.encoding = r.apparent_encoding

        re = pd.read_html(r.text, header=None)

        print("End requesting.")

        print("Begin selecting...")

        all = re[9]

        # 公司代號
        stock = all.loc[:, 0]
        stock = stock.drop([0])

        # 毛利率
        gm = all.loc[:, 3]
        gm = gm.drop([0])

        # 營業收益率
        opm = all.loc[:, 4]
        opm = opm.drop([0])

        # 營業收入
        oi = all.loc[:, 2]
        oi = oi.drop([0])

        '''
        #營業收益
        op = opm * oi 

        op.columns = ["營業收益"]
        '''
        results = pd.concat([stock, gm, opm, oi], axis=1)
        results.columns = ["公司代號", "毛利率", "營業收益率", "營業收入"]

        results.drop(results.loc[results['公司代號'] == '公司代號'].index, inplace=True)

        # ----------------------Sqlite----------------------
        print("================Begin to write table================")
        conn = sqlite3.connect('db1.db')
        cursor = conn.cursor()
        tbname = "tb_" + str(year) + "_" + str(season)
        cursor.execute('CREATE TABLE ' + tbname + "(公司代號, 毛利率, 營業收益率, 營業收入)")

        results.to_sql(tbname, conn, if_exists='append', index=False)
        conn.commit()
        print("================End of writing table================")

print("Done")

endtime = dt.datetime.now()

print("Process time:", endtime - starttime)
#營益分析表https://ithelp.ithome.com.tw/articles/10204773
#毛利率季增率>0(5)       season2/season1   -1
#毛利率年增率>0(5)       year2/year1            -1
#營業收益季增率>0(5)   營業收益率*營業收入(season2/season1) -1
#營業收益年增率>0(5)   營業收益率*營業收入(year2/year1) -1

#穩定性
#營業活動現金流量>0(5)
#現金流量表
url = "https://mops.twse.com.tw/mops/web/t05st39"
#營業利益>0(5)
#綜合損益表
url = "https://mops.twse.com.tw/mops/web/t164sb04"
#本期淨利>0(5)
#同上
#過去五年發放現金股利(5)
#待查

#安全性
#流動比率>100%(5)
#財務分析資料
url = "https://mops.twse.com.tw/mops/web/t05st22"
#負債比率<50%(5)
#同上

#價值性
#本益比_越低分數越高(15)
url = "https://www.twse.com.tw/zh/page/trading/exchange/BWIBBU_d.html"
#股價淨值比_越低分數越高(5)
#同上
#現金殖利率_越高分數越高(10)
