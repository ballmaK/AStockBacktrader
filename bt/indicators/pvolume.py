import backtrader as bt
from backtrader import Indicator

class MMV(Indicator):
    
    lines = ('maxvolume', 'minvolume',)
    
    params = (('period',90),)
    
    def __init__(self, data):
        self.data = data
        self.lines.minvolume = bt.talib.MIN(self.data.volume, timeperiod=self.params.period)
        
        self.lines.maxvolume = bt.talib.MAX(self.data.volume, timeperiod=self.params.period)
        
        super(MMV, self).__init__(data=self.data)
        
class MMVP(Indicator):
    
    lines = ('maxvp', 'minvp', )
    params = (('period',90),)
    
    def __init__(self, data):
        self.data = data
        self.minidx = bt.talib.MININDEX(self.data.volume, timeperiod=self.params.period)
        self.maxidx = bt.talib.MAXINDEX(self.data.volume, timeperiod=self.params.period)
        super(MMVP, self).__init__(data=self.data)
        
    def next(self):
        
        self.lines.minvp[0] = self.data.close.array[int(self.minidx[0])]
        self.lines.maxvp[0] = self.data.close.array[int(self.maxidx[0])]
        
class BAVGV(Indicator):
    
    lines = ('bavgv', )
    params = (('period', 5), )
    
    def __init__(self,data):
        self.data=data
        self.lines.bavgv = bt.indicators.MovingAverageSimple(self.data.volume, period=self.p.period)
        super(BAVGV).__init__(data=self.data)
        
class VPR(Indicator):
    
    lines = ('vpr', )
        
    def __init__(self, data):
        self.data=data
        self.lines.vpr = self.data.close / self.data.volume
        
        super(VPR, self).__init__(data=self.data)
        
class MVPR(Indicator):
    
    lines = ('minvpr', 'maxvpr', )
    
    params = (('period', 5), )
    
    def __init__(self, data):
        self.data=data
        self.pv = MMV(data=self.data, period=self.params.period)
        self.mmvp = MMVP(data=self.data, period=self.p.period)
        
        super(MVPR, self).__init__(data=self.data)
        
    def next(self):
        self.lines.maxvpr[0] = self.mmvp.lines.maxvp[0]/self.pv.lines.maxvolume[0] * self.data.volume[0]
        self.lines.minvpr[0] = self.mmvp.lines.minvp[0]/self.pv.lines.minvolume[0] * self.data.volume[0]
        
class MPP(Indicator):
    
    lines = ('maxpp', 'minpp')
    
    params = (('period', 5), )
    
    def __init__(self, data):
        self.data=data
        self.pv = MMV(data=self.data, period=self.params.period)
        self.mmvp = MMVP(data=self.data, period=self.p.period)
        
        super(MPP, self).__init__(data=self.data)
        
    def next(self):
        
        self.lines.maxpp[0] = self.mmvp.lines.maxvp[0]/self.pv.lines.maxvolume[0] * self.data.volume[0]
        self.lines.minpp[0] = self.mmvp.lines.minvp[0]/self.pv.lines.minvolume[0] * self.data.volume[0]

        # print(self.lines.mpp[0],self.mmvp.lines.maxvp[0],self.pv.lines.maxvolume[0], self.data.volume[0])
        
class PVVP(Indicator):
    
    lines = ('pvvpb', 'pvvps', 'vsma', 'maxpp', 'minpp', )
    
    params = (('period', 90), ('sr', 0.9), ('br', 0.8), ('rr', 2),)
    
    def __init__(self, data):
        self.data = data
        self.mmvp = MMVP(data=self.data, period=self.p.period)
        self.pv = MMV(data=self.data, period=self.params.period)
        self.vpr = VPR(data=self.data)
        self.lines.vsma = self.data.close / bt.indicators.MovingAverageSimple(self.data.volume, period=10) * self.data.volume
        self.mpp = MPP(data=self.data, period=self.p.period)
        self.lines.maxpp = self.mpp.lines.maxpp
        self.lines.minpp = self.mpp.lines.minpp
        # self.lines.mpp = self.mpp
        super(PVVP, self).__init__(data=self.data)
        
    def next(self):
        sigb = (self.pv.lines.minvolume[0] * self.vpr.lines.vpr[0] >= self.data.close[0]) and (self.mmvp.lines.minvp[0] >= self.data.close[0])
        # sigb = (self.lines.maxpp[0]/self.data.close[0] <= 0.15) and (self.pv.lines.minvolume[0] * self.vpr.lines.vpr[0] >= self.data.close[0]) and (self.mmvp.lines.minvp[0] >= self.data.close[0])

        sigs = self.data.close[0] >= (self.pv.lines.maxvolume[0] * self.vpr.lines.vpr[0] * self.p.sr) or (self.mmvp.lines.minvp[0] * self.p.rr <= self.lines.vsma[0])
        # sigs = self.lines.minpp[0]/self.data.close[0] < 1.1
        # if sigb:
        #     print(sigb, self.mmvp.lines.minvp[0])
        self.lines.pvvpb[0] = self.data.close[0] if sigb else 0
        # if sigs:
        #     print(sigs, self.mmvp.lines.maxvp[0])
        self.lines.pvvps[0] = self.data.close[0] if sigs else 0
        
        
    
    