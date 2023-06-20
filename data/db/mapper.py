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
    sql = "select * from %s where code='%s' and date >= '%s' and date <= '%s'" % (constants.STOCK_DAILY_TABLE_NAME,code, start_date, end_date)
    # print(sql)
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return ''
    return df

def select_stock_trade_by_date(fromdate):
    sql = "SELECT \
            buy.exe_date AS buy_date, \
            buy.code, \
            sb.name, \
            FORMAT(sid.money / sid.turnover, 2) + 'E' AS 'FMV', \
            sid.PE,\
            sid.PB,\
            sid.ind_name,\
            IFNULL(sell.exe_date, '--') AS sell_date,\
            buy.last_order_price AS buy_price,\
            IFNULL(sell.last_order_price, '--') AS sell_price,\
            sd.close AS now_price,\
            IF(ISNULL(sell.last_order_price),\
                FORMAT((sd.close - buy.last_order_price) / buy.last_order_price * 100,\
                    2),\
                FORMAT((sell.last_order_price - buy.last_order_price) / buy.last_order_price * 100,\
                    2)) AS profit\
        FROM\
            stock_daily_result AS buy\
                LEFT JOIN\
            stock_daily_result AS sell ON buy.code = sell.code\
                AND buy.exe_date < sell.exe_date\
                AND sell.last_order_type = 'SELL'\
                LEFT JOIN\
            stock_daily sd ON buy.code = sd.code\
                LEFT JOIN\
            stock_base sb ON buy.code = sb.code\
                LEFT JOIN\
            (SELECT \
                *\
            FROM\
                stock_industry_detail\
            WHERE\
                date = (SELECT \
                        date\
                    FROM\
                        stock_data.stock_industry_detail\
                    GROUP BY date\
                    ORDER BY date DESC\
                    LIMIT 1)) sid ON sb.symbol = sid.symbol\
        WHERE\
            buy.last_order_type = 'BUY'\
                AND buy.exe_date > '%s'\
                AND buy.rnorm100 > 20\
                AND sd.date = '%s'\
                AND sid.PE > 0" % (fromdate, get_lastest_trade_date())
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

def select_industry_data_by_date(date):
    sql = 'select * from %s where date="%s"' % (constants.STOCK_INDUSTRY_TABLE_NAME, date)
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return pd.DataFrame()
    return df

def select_industry_data_detail(date, industry_code):
    sql = 'select * from %s where date="%s" and ind_code="%s"' % (constants.STOCK_INDUSTRY_DETAIL_TABLE_NAME, date, industry_code)
    try:
        df = pd.read_sql(sql=sql, con=base.engine())
    except Exception as e:
        print(e)
        return pd.DataFrame()
    return df