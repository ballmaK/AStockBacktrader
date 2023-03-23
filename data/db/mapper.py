import pandas as pd
from db import common

def getOneDayTradeData(date):
    sql = "select * from stock_zh_a_daily where date='%s' order by date desc" % date
    try:
        df = pd.read_sql(sql=sql, con=common.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def isTradeDate(date):
    dates = getTradeDates(None, None)
    return date in dates

def getTradeDates(start_date, end_date):
    sql = "select distinct date from stock_zh_a_daily where code='sh600000' order by date desc"
    try:
        df = pd.read_sql(sql=sql, con=common.engine())
    except Exception as e:
        print(e)
        return ''
    return df['date'].to_list()
    
def getMaxTradeDateNDaysBefore(n):
    sql = "select distinct date from stock_zh_a_daily where code='sh600000' order by date desc"
    try:
        df = pd.read_sql(sql=sql, con=common.engine())
    except Exception as e:
        print(e)
        return ''
    return df['date'].to_list()[n]

def getMaxTradeDate():
    sql = "select distinct date from stock_zh_a_daily where code='sh600000' order by date desc"
    try:
        df = pd.read_sql(sql=sql, con=common.engine())
    except Exception as e:
        print(e)
        return ''
    return df['date'].to_list()[0]

def select_all_code():
    sql = 'select distinct code from stock_zh_a_daily'
    try:
        df = pd.read_sql(sql=sql, con=common.engine())
    except Exception as e:
        print(e)
        return ''
    return df['code'].to_list()

def select_data_by_code(code, limit):
    if limit != None:
        sql = 'select * from stock_zh_a_daily where code="%s" order by date desc limit %s' % (code, limit)
    else:
        sql = 'select * from stock_zh_a_daily where code="%s" order by date desc' % (code)
    try:
        df = pd.read_sql(sql=sql, con=common.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def select_data(code, date, limit):
    if limit != None:
        sql = "select * from stock_zh_a_daily where code='%s' and TIMESTAMP(date) <= TIMESTAMP('%s') order by date desc limit %s" % (code, date, limit)
    else:
        sql = "select * from stock_zh_a_daily where code='%s' and TIMESTAMP(date) <= TIMESTAMP('%s') order by date desc" % (code, date)
    # print(sql)
    try:
        df = pd.read_sql(sql=sql, con=common.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def select_data_between_date(code, start_date, end_date):
    sql = "select * from stock_zh_a_daily where code='%s'and TIMESTAMP(date) >= TIMESTAMP('%s') and TIMESTAMP(date) <= TIMESTAMP('%s')" % (code, start_date, end_date)
    # print(sql)
    try:
        df = pd.read_sql(sql=sql, con=common.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def select_data_by_date(date):
    sql = 'select * from stock_zh_a_daily where date="%s" order by date' % date
    try:
        df = pd.read_sql(sql=sql, con=common.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def select_stock_data_by_date(code, date):
    sql = 'select * from stock_zh_a_daily where date="%s" and code="%s" order by date' % (date, code)
    try:
        df = pd.read_sql(sql=sql, con=common.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def select_trade_by_id(trade_id):
    sql = 'select * from stock_trade_log where trade_id="%s"' % trade_id
    try:
        df = pd.read_sql(sql=sql, con=common.engine())
    except Exception as e:
        print(e)
        return ''
    return df