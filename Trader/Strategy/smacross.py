import backtrader as bt
class SmaCross(bt.Strategy):
    
    # 設定交易參數
    params = dict(ma_period_short=5,ma_period_long=10)

    def __init__(self):
        # 均線交叉策略
        sma1 = bt.ind.SMA(period=self.p.ma_period_short) #sma1 = 五日線
        sma2 = bt.ind.SMA(period=self.p.ma_period_long)  #sma2 = 十日線
        self.crossover = bt.ind.CrossOver(sma1, sma2)
        

    def next(self):
        if self.crossover > 0:
            self.buy()
        elif self.crossover < 0:
            self.close()
