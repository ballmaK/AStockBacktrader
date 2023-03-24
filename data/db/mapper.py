import pandas as pd

from . import base
from . import constants

def getOneDayTradeData(date):
    sql = "select * from %s where date='%s' order by date desc" % (constants.STOCK_DAILY_TABLE_NAME ,date)
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def isTradeDate(date):
    dates = getTradeDates(None, None)
    return date in dates

def getTradeDates(start_date, end_date):
    sql = "select distinct date from %s where code='sh600000' order by date desc" % constants.STOCK_DAILY_TABLE_NAME
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return ''
    return df['date'].to_list()
    
def getMaxTradeDateNDaysBefore(n):
    sql = "select distinct date from %s where code='sh600000' order by date desc" % constants.STOCK_DAILY_TABLE_NAME
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return ''
    return df['date'].to_list()[n]

def get_lastest_trade_date():
    sql = "select distinct date from %s where code='sh600000' order by date desc" % constants.STOCK_DAILY_TABLE_NAME
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return ''
    return df['date'].to_list()[0]

def select_all_code():
    sql = 'select distinct code from %s' % constants.STOCK_BASE_TABLE_NAME
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return ''
    return df['code'].to_list()

def select_data_by_code(code, limit):
    if limit != None:
        sql = 'select * from %s where code="%s" order by date desc limit %s' % (constants.STOCK_DAILY_TABLE_NAME, code, limit)
    else:
        sql = 'select * from %s where code="%s" order by date desc' % (constants.STOCK_DAILY_TABLE_NAME, code)
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def select_data(code, date, limit):
    if limit != None:
        sql = "select * from %s where code='%s' and TIMESTAMP(date) <= TIMESTAMP('%s') order by date desc limit %s" % (constants.STOCK_DAILY_TABLE_NAME, code, date, limit)
    else:
        sql = "select * from %s where code='%s' and TIMESTAMP(date) <= TIMESTAMP('%s') order by date desc" % (constants.STOCK_DAILY_TABLE_NAME, code, date)
    # print(sql)
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def select_data_between_date(code, start_date, end_date):
    sql = "select * from %s where code='%s'and TIMESTAMP(date) >= TIMESTAMP('%s') and TIMESTAMP(date) <= TIMESTAMP('%s')" % (constants.STOCK_DAILY_TABLE_NAME,code, start_date, end_date)
    # print(sql)
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def select_data_by_date(date):
    sql = 'select * from %s where date="%s" order by date' % (constants.STOCK_DAILY_TABLE_NAME, date)
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def select_stock_data_by_date(code, date):
    sql = 'select * from %s where date="%s" and code="%s" order by date' % (constants.STOCK_DAILY_TABLE_NAME, date, code)
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def select_trade_by_id(trade_id):
    sql = 'select * from stock_trade_log where trade_id="%s"' % trade_id
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return ''
    return df