from datetime import datetime

# import datetime as dt
import akshare as ak
import backtrader as bt
import matplotlib.pyplot as plt  # 由于 Backtrader 的问题，此处要求 pip install matplotlib==3.2.2
import pandas as pd
# import policy.indicators

import bt.indicators as btind
from backtrader.utils.py3 import iteritems
from pandas import DataFrame as DF

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置画图时的中文显示
plt.rcParams["axes.unicode_minus"] = False  # 设置画图时的负号显示


class LightVolume(bt.Strategy):
    """
    主策略程序
    """
    alias = ('Light_Volume',)
    
    params = (("period",45),
              ('br', 0.90),
              ('sr', 0.80),
              ('rr', 2),
              ('tp', None),
              ('sl', None),
              ('_pvvp', dict()),
              ('printlog', False),)  # 全局设定交易策略的参数, period是 MA 均值的长度

    def __init__(self):
        """
        初始化函数
        分别针对成交量60、90、120、180、240日内的最小值和当前成交量做比较, 研究其同后市股价涨跌的相关性
        """
        self.orders = []
        self.data_close = self.datas[0].close  # 指定价格序列
        self.data_vol = self.datas[0].volume
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        
        
        # self._pvvp = [btind.pvolume.PVVP(period=self.p.period, br=self.p.br, sr=self.p.sr, rr=self.p.rr) for data in self.datas]
        self.lvs = dict()
        for data in self.datas:
            # print(data._name,'0000')
            # print(dir(btind.pvolume.PVVP))
            self.lvs[data._name] = btind.pvolume.PVVP(data=data, period=self.p.period, br=self.p.br, sr=self.p.sr, rr=self.p.rr)
        
    def next(self):
        """
        主逻辑
        """

        for i, d in enumerate(self.datas):
            # self.log(f'收盘价, {data_close[0]}')  # 记录收盘价
            if self.order:  # 检查是否有指令等待执行,
                return
            # 检查是否持
            
            # print(self.broker.getposition(d), d._name)
            if not self.broker.getposition(d):  # 没有持仓
                # 执行买入条件判断：当日成交量接近目标成交量
                # if buy_rate >= self.params.br and self.data_close[0] <= min_price:
                # print(d._name, '----')
                if self.lvs[d._name].pvvpb > 0:
                    # 执行买入
                    self.order = self.buy(data=d)
                else:
                    pass
            else:
                # 执行卖出条件判断：收盘价格跌破15日均线
                # 止盈止损
                # shouldSell = ((self.data_close[0] - self.position.price)/self.position.price < -0.1)# or ((self.data_close[0] - self.position.price)/self.position.price >= 0.5)
                take_profit  = (d.close[0] - self.position.price)/self.position.price*100 >= self.p.tp if self.p.tp else False
                stop_less = (d.close[0] - self.position.price)/self.position.price*100 < -self.p.sl if self.p.sl else False
                if self.lvs[d._name].pvvps[0] > 0: #or stop_less or take_profit:
                    # 执行卖出
                    self.order = self.sell(data=d)
                else:
                    pass
                    # self.log("HOLD,%.2f %.2f %.2f" % (self.data_close[0], buy_rate, sell_rate))

    def log(self, txt, dt=None, do_print=False, do_persistence=False):
        """
        Logging function fot this strategy
        """
        if self.params.printlog or do_print:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))
        
        # if self.params.persistence or do_persistence:
        #     pass

    def notify_order(self, order):
        """
        记录交易执行情况
        """
        # 如果 order 为 submitted/accepted,返回空
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 如果order为buy/sell executed,报告价格结果
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f"BUY:{order.data._name},PRICE:{order.executed.price},\
                COST:{order.executed.value},\
                COMM:{order.executed.comm}"
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    f"SELL:{order.data._name},PRICE：{order.executed.price},\
                COST: {order.executed.value},\
                COMM{order.executed.comm}"
                )
            self.bar_executed = len(self)
            side = 'BUY' if order.isbuy() else 'SELL'
            self.orders.append({
                'datetime': order.data.datetime.datetime(),
                'ref': order.ref,
                'size': abs(order.size),
                'price': order.executed.price,
                'value': order.executed.value,
                'commission': order.executed.comm,
                'side': side,
                'price_now': order.data.close.array[-1],
                'stock': order.data._name,
            })

            # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("交易失败")
        self.order = None

    def notify_trade(self, trade):
        """
        记录交易收益情况
        """
        if not trade.isclosed:
            return
        self.log(f"策略收益：毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}")

    def stop(self):
        """
        回测结束后输出结果
        """
        # self.log("(周期天数 %2d日)(RB %2f)(RS %2f) 期末总资金 %.2f" % (self.params.period, self.params.rate_buy, self.params.rate_sell, self.broker.getvalue()), do_print=True)
        # print(self.broker.startingcash, self.analyzers.mysharpe.get_analysis())
        # print(DF.from_records(iteritems(self.analyzers.pyfolio.get_analysis())))
        # for i, a in enumerate(self.analyzers):
        #     # print(dir(a))
        #     # print(dir(a.get_analysis()))
        #     print(a)
        #     if isinstance(a, bt.analyzers.PyFolio):
        #         print('found pyfolio analysis')
        #         # analyzer = self.analyzers.getbyname('pyfolio',)
        #         # print(dir(a))
        #         print(a.get_pf_items(),'=================')
        #         # returns, positions, transactions, gross_lev = a.get_pf_items()
        #         # print(returns, positions, transactions, gross_lev)

        #     if isinstance(a, bt.analyzers.Returns):
        #         analyzer = self.analyzers.getbyname('returns',)
        #         print('found pyfolio returns')
            
        #         print(dir(analyzer))
        #         for k, v in analyzer.get_analysis().items():
        #             print('{}: {}'.format(k, v))
        pass
