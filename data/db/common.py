#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import sys
import os
import akshare as ak

# sys.path.append("../..")
import utils.timeutils as timeutils
import utils.threadpool as threadpool

from datetime import datetime
from . import base
from . import mapper
from . import constants

def update_stock_daily(stock=None, fromdate=None, todate=None, adjust='hfq'):
    if not stock:
        stocks = select_all_stocks()
    else:
        stocks = [stock]
    
    if not fromdate:
        lastest = datetime.strptime(get_lastest_trade_date(), timeutils.DATE_FORMAT_TO_DAY)
        start_date = timeutils.get_next_day(lastest)
    else:
        fromdate = str(fromdate)
        start_date = datetime.strptime(fromdate, timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)
    
    if not todate:
        end_date = datetime.today()
    else:
        todate = str(todate)
        end_date = datetime.strptime(todate, timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)
        
    q_size = len(stocks)
    if datetime.today() <= end_date:
        print("** 更新时间 [%s] **" % end_date.strftime(timeutils.DATE_FORMAT_TO_DAY))
        if datetime.now().hour > constants.UPDATE_TIME_DAILY_LIMIT:
            print(f'** 开始更新日线数据 [{start_date.strftime(timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)} - {end_date.strftime(timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)}][{adjust}] **')
            pool = threadpool.ThreadPool(10, q_size=q_size, resq_size=q_size)
            args = [([stock, start_date, end_date, adjust], {}) for stock in stocks]
            requests = threadpool.makeRequests(__init_stock_daily, args)
            [pool.putRequest(req) for req in requests]
            pool.wait()
        else:
            print(f'** 更新时间不能早于 {end_date.strftime(timeutils.DATE_FORMAT_TO_DAY)} {constants.UPDATE_TIME_DAILY_LIMIT} 点')
    else:
        print(f'** 开始更新日线数据 [{start_date.strftime(timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)} - {end_date.strftime(timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)}][{adjust}] **')
        pool = threadpool.ThreadPool(10, q_size=q_size, resq_size=q_size)
        args = [([stock, start_date.strftime(timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH), end_date.strftime(timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH), adjust], {}) for stock in stocks]
        requests = threadpool.makeRequests(__init_stock_daily, args)
        [pool.putRequest(req) for req in requests]
        pool.wait()

def select_all_stocks():
    return mapper.select_all_code()

def select_data(stock, fromdate, todate):
    pass

def select_random_stock_data(fromdate, todate, stock_num=10):
    pass

def get_lastest_trade_date():
    return mapper.get_lastest_trade_date()

def init_stock_info():
    print('** 更新股票基础数据 **')
    df = ak.stock_zh_a_spot()
    df['code'] = df['代码']
    df['symbol'] = df['代码'].map(lambda x: x[2:])
    df['name'] = df['名称']
    stock_df = df[['code', 'symbol', 'name']]
    stock_df.set_index('code', inplace=True)
    print(stock_df)
    if not stock_df.empty:
        base.insert_db(stock_df, constants.STOCK_BASE_TABLE_NAME, True, "`code`")
        

def __init_stock_daily(stock, start_date, end_date, adjust):
    try:
        # print('-------------------------------- ', stock, ' ---------------------------------')
        # exist_df = mapper.select_data_by_code(stock, 1)
        # if exist_df.empty:
        df = ak.stock_zh_a_daily(symbol=stock, start_date=start_date, end_date=end_date, adjust=adjust)
        # hotfix stock code
        #df = ak.stock_zh_a_hist(symbol=stock[2:], period="daily", start_date=start_date, end_date=end_date, adjust=adjust)

        # df.columns = ['code', 'date', 'open', 'high', 'low', 'close', 'volume', 'outstanding_share', 'turnover']
        # print(stock, df['date'].count())
        # print(df)
        df['code'] = stock
        df['date'] = df['date'].map(timeutils.reformat_date)
        df = df[['code', 'date', 'open', 'high', 'low', 'close', 'volume', 'outstanding_share', 'turnover']]
        
        df.set_index('date', inplace=True)
        # df.drop('index', axis=1, inplace=True)
        # print(df)
        # 删除index，然后和原始数据合并。
        print('[UPDATING][%s][%s - %s][%s][%s rows]' % (stock, start_date, end_date, adjust, df['code'].count()))
        base.insert_db(df, constants.STOCK_DAILY_TABLE_NAME, True, "`date`,`code`")
        # else:
            # print('[%s] already exist, pass' % stock)
    except Exception as e:
        print('error', stock, e)
        
if __name__ == '__main__':
    update_stock_daily()