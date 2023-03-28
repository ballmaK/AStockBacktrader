import pandas as pd
from data.db import common
from backtrader.feeds import pandafeed

from utils.timeutils import *

class DBDataBase(pandafeed.PandasData):
    
    params = (
        ('dataname', 'localdbdata'),
        ('name', None),
        ('stock', None),
        ('compression', 1),
        ('timeframe', 'days'),
        ('fromdate', None),
        ('todate', None),
    )
    
    def __init__(self):
        self.p.name = self.p.dataname
        df = common.select_stock_daily(stock=self.p.dataname, 
                                       fromdate=self.p.fromdate.strftime(DATE_FORMAT_TO_DAY_WITHOUT_DASH), 
                                       todate=self.p.todate.strftime(DATE_FORMAT_TO_DAY_WITHOUT_DASH)) 
        df['open'] = pd.to_numeric(df['open'])
        df['close'] = pd.to_numeric(df['close'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['volume'] = pd.to_numeric(df['volume'])
        df.index = pd.to_datetime(df['date'])
        self.p.dataname=df
        
        super(DBDataBase, self).__init__()
        