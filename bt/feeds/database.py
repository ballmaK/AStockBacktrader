from data.db import common
from backtrader.feed import DataBase

from utils.timeutils import *

class LocalDataBase(DataBase):
        
    params = (
        ('dataname', 'localdbdata'),
        ('name', None),
        ('stock', None),
        ('compression', 1),
        ('timeframe', 'days'),
        ('fromdate', None),
        ('todate', None),
    )
    
    def __init__(self, **kwargs):
        super(LocalDataBase, self).__init__()
    
    # 定义加载数据的方法
    def _load(self):
        # 查询数据
        df = common.select_stock_daily(stock=self.p.stock, 
                                       fromdate=self.p.fromdate.strftime(DATE_FORMAT_TO_DAY_WITHOUT_DASH), 
                                       todate=self.p.todate.strftime(DATE_FORMAT_TO_DAY_WITHOUT_DASH))        
        
        # 加载 Pandas DataFrame 中的数据
        # df = self.p.dataname
        
        # 将 DataFrame 的每一行转换为一个字典，然后添加到 self.lines 里面去
        for ix, row in df.iterrows():
            dt = self.lines.datetime.datetime(ix.year, ix.month, ix.day)
            line = tuple([dt] + [row[col] for col in self.cols[1:]])
            self.lines[0].append(line)
            
        # 设置好相关信息
        self.firstask = 0.0  # 第一次请求时的卖价
        self.decimals = 2  # 价格小数位数
        self.volume_decimals = 0  # 成交量小数位数
        
    def setenvironment(self, env):
        '''Keep a reference to the environment'''
        self._env = env