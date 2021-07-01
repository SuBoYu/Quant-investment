import pandas as pd
import requests

#營收成長性
url = "https://mops.twse.com.tw/nas/t21/sii/t21sc03_103_2_0.html"
#月報https://www.finlab.tw/%E8%B6%85%E7%B0%A1%E5%96%AE%E7%94%A8python%E6%8A%93%E5%8F%96%E6%AF%8F%E6%9C%88%E7%87%9F%E6%94%B6/
#月營收月增率>0(5)
#月營收年增率>0(5)
#累計營收年增率>0(10)

#獲利成長性
url = "https://mops.twse.com.tw/mops/web/t163sb06"
#營益分析表https://ithelp.ithome.com.tw/articles/10204773
#毛利率季增率>0(5)
#毛利率年增率>0(5)
#營業收益季增率>0(5)
#營業收益年增率>0(5)

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
