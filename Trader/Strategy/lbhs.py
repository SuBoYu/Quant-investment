import backtrader as bt

class MyStrategy(bt.Strategy):

    def next(self):     
        if self.data[0] < 0.95*(self.data[-1]+self.data[-2]+self.data[-3]+self.data[-4]+self.data[-5])/5:
            self.buy()
        
        elif self.data[0] > 1.05*(self.data[-1]+self.data[-2]+self.data[-3]+self.data[-4]+self.data[-5])/5:
            self.sell()
