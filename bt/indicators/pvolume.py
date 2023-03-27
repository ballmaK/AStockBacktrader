import backtrader as bt
from backtrader import Indicator

class MMV(Indicator):
    
    lines = ('maxvolume', 'minvolume',)
    
    params = (('period',90),)
    
    def __init__(self):
        
        self.lines.minvolume = bt.talib.MIN(self.data.volume, timeperiod=self.params.period)
        
        self.lines.maxvolume = bt.talib.MAX(self.data.volume, timeperiod=self.params.period)
        
        super(MMV, self).__init__()
        
class MMVP(Indicator):
    
    lines = ('maxvp', 'minvp', )
    params = (('period',90),)
    
    def __init__(self):
        self.minidx = bt.talib.MININDEX(self.data.volume, timeperiod=self.params.period)
        self.maxidx = bt.talib.MAXINDEX(self.data.volume, timeperiod=self.params.period)
        super(MMVP, self).__init__()
        
    def next(self):
        
        self.lines.minvp[0] = self.data.close.array[int(self.minidx[0])]
        self.lines.maxvp[0] = self.data.close.array[int(self.minidx[0])]
        
class BAVGV(Indicator):
    
    lines = ('bavgv', )
    params = (('period', 5), )
    
    def __init__(self):
        
        self.lines.bavgv = bt.indicators.MovingAverageSimple(self.data.volume, period=self.p.period)
        super(BAVGV).__init__()
        
class VPR(Indicator):
    
    lines = ('vpr', )
    
    params = (('br', 0.9), ('sr', 0.8), )
    
    def __init__(self):
        self.lines.vpr = self.data.close / self.data.volume
        
        super(VPR, self).__init__()
        
class PVVP(Indicator):
    
    lines = ('pvvpb', 'pvvps', 'vsma')
    
    params = (('period', 90), ('sr', 0.9), ('br', 0.8), )
    
    def __init__(self):
        
        self.mmvp = MMVP(self.data, period=self.p.period)
        self.pv = MMV(self.data, period=self.params.period)
        self.vpr = VPR(self.data, sr=self.params.sr, br=self.params.br)
        self.lines.vsma = self.data.close / bt.indicators.MovingAverageSimple(self.data.volume, period=10) * self.data.volume
                
        # self.lines.pvvpb = pv.lines.minvolume * vpr.lines.vpr
        
        # self.lines.pvvps = pv.lines.maxvolume * vpr.lines.vpr
        # self.lines.mmvp = self.mmvp.lines.minvp
        
        # self.sigb[0] = False#(self.pv.lines.minvolume[0] * self.vpr.lines.vpr[0] >= self.data.close[0]) and (self.mmvp.lines.minvp[0] >= self.data.close[0])
        
        # self.lines.pvvpb = self.data.close if self.sigb else 0
        
        # self.lines.pvvps = self.data.close >= (self.pv.lines.maxvolume * self.vpr.lines.vpr * self.p.sr)
        
        # vpr = self.data.close / self.data.volume
        
        # self.lines.pvvpb = pv.lines.minvolume * self.data.close / self.data.volume
        
        # self.lines.pvvps = pv.lines.maxvolume * self.data.close / self.data.volume
        
        # buy_rate = self.minvol[0]/self.datas[0].volume > self.p.br = self.lines.PVVPB / self.data.close > 0.9
        # sell_rate = self.datas[0].volume/self.maxvol[0] > self.p.sr = self.data.close / self.lines.PPVPS > 0.8
        
        # buy_rate = self.minvol[0]/self.datas[0].volume = self.lines.PVVPB / self.data.close > self.p.br
        
        # sell_rate = self.datas[0].volume/self.maxvol[0] = self.data.close / self.lines.PVVPS > self.p.sr
        
        # pv.lines.minvolume * self.data.close / self.data.volume >= self.data_close[0] * self.p.br
        
        # buy_rate >= self.params.br and self.data_close[0] <= min_price
        
        # self._pvvp.pvvpb >= self.data_close[0] * self.p.br
        
    def next(self):
        sigb = (self.pv.lines.minvolume[0] * self.vpr.lines.vpr[0] >= self.data.close[0]) and (self.mmvp.lines.minvp[0] >= self.data.close[0])
        sigs = self.data.close[0] >= (self.pv.lines.maxvolume[0] * self.vpr.lines.vpr[0] * self.p.sr) or (self.mmvp.lines.minvp[0] * 2 <= self.lines.vsma[0])
        if sigb:
            print(sigb, self.mmvp.lines.minvp[0])
        self.lines.pvvpb[0] = self.data.close[0] if sigb else 0
        if sigs:
            print(sigs, self.mmvp.lines.maxvp[0])
        self.lines.pvvps[0] = self.data.close[0] if sigs else 0
        
        
    
    