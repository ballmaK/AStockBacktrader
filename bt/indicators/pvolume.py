import backtrader as bt
from backtrader import Indicator

class MMVIDX(Indicator):
    
    lines = ('maxvolume', 'minvolume',)
    
    params = (('period',90),)
    
    def __init__(self):
        
        self.lines.minvidx = bt.talib.MININDEX(self.data.volume, timeperiod=self.params.period)
        
        self.lines.maxvidx = bt.talib.MAXINDEX(self.data.volume, timeperiod=self.params.period)
        
        super(MMVIDX, self).__init__()
        
class VPR(Indicator):
    
    lines = ('vpr', )
    
    params = (('br', 0.9), ('sr', 0.8), )
    
    def __init__(self):
        self.lines.vpr = self.data.close / self.data.volume
        
        super(VPR, self).__init__()
        
class PVVP(Indicator):
    
    lines = ('pvvpb', 'pvvps', 'mpb', 'mps')
    
    params = (('period', 90), ('sr', 0.9), ('br', 0.8), )
    
    def __init__(self):
        
        pv = MMVIDX(self.data, period=self.params.period)
        vpr = VPR(self.data, sr=self.params.sr, br=self.params.br)
        
        pvvpb = pv.lines.minvolume * vpr.lines.vpr
        
        pvvps = pv.lines.maxvolume * vpr.lines.vpr
        
        last_min_price = 
        
        self.lines.sigb = pvvpb >= self.data.close and last_min_price >= self.data.close
        
        self.lines.sigs = pv.lines.maxvolume * vpr.lines.vpr
        
        # vpr = self.data.close / self.data.volume
        
        # self.lines.pvvpb = pv.lines.minvolume * self.data.close / self.data.volume
        
        # self.lines.pvvps = pv.lines.maxvolume * self.data.close / self.data.volume
        
        # buy_rate = self.minvol[0]/self.datas[0].volume > self.p.br = self.lines.PVVPB / self.data.close > 0.9
        # sell_rate = self.datas[0].volume/self.maxvol[0] > self.p.sr = self.data.close / self.lines.PPVPS > 0.8
        
        # buy_rate = self.minvol[0]/self.datas[0].volume = self.lines.PVVPB / self.data.close > self.p.br
        
        # sell_rate = self.datas[0].volume/self.maxvol[0] = self.data.close / self.lines.PVVPS > self.p.sr
        
        pv.lines.minvolume * self.data.close / self.data.volume >= self.data_close[0] * self.p.br
        
        
        
    
    