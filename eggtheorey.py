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