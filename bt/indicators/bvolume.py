import backtrader as bt
from backtrader import Indicator
        
class STDV(Indicator):
    
    lines = ('buy', 'sell', )
    params = (('period', 90), ('br1', 3), ('br2', 1.1), ('sr', 1.1), )
    
    def __init__(self, data):
        self.data = data
        self.stdv = bt.indicators.StdDev(self.data.volume, period=self.p.period)
        self.smaClose = bt.indicators.SMA(self.data.close, period=self.p.period)
        self.stdp = bt.indicators.StdDev(self.data.close, period=self.p.period)
        self.avgv = bt.indicators.Average(self.data.volume, period=self.p.period)
        self.avgp = bt.indicators.Average(self.data.close, period=self.p.period)
        super(STDV, self).__init__(data=self.data)
        
    def next(self):
        # print(self.data.close[0], round(self.avgp[0], 2), round(self.avgv[0]), self.data.volume[0], round(self.data.volume[0]/self.avgv[0]))
        # if self.stdv[0]/self.data.volume[0] < 0.2 and self.data.close[0]/self.smaClose[0]<=1.05:
        if self.data.volume[0]/self.avgv[0] >= self.p.br1 and self.data.close[0] <= self.avgp[0] * self.p.br2:
            self.lines.buy[0] = self.data.close[0]
        else:
            self.lines.buy[0] = 0
            
        if self.data.close[0]/self.avgp[0] >= self.p.sr:
            self.lines.sell[0] = self.data.close[0]
        else:
            self.lines.sell[0] = 0
        
        
    
    