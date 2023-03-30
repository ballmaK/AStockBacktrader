import pandas as pd
from data.db import common
from backtrader.feeds import pandafeed

from utils.timeutils import *
from utils.datautils import *

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

        self.p.dataname=df_convert(df)
        
        super(DBDataBase, self).__init__()
        