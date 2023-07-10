#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import random
import akshare as ak
import traceback
import pandas as pd
# import ttl_cache

# sys.path.append("../..")
from functools import cache
import utils.timeutils as timeutils
import utils.threadpool as threadpool

from datetime import datetime
from . import base
from . import mapper
from . import constants
from utils.log import logger

data_cache = None

def update_stock_daily(stock=None, fromdate=None, todate=None, adjust='hfq'):
    if stock == 'all':
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
        # print("** 更新时间 [%s] **" % end_date.strftime(timeutils.DATE_FORMAT_TO_DAY))
        msg = "** 更新时间 [%s] **" % end_date.strftime(timeutils.DATE_FORMAT_TO_DAY)
        logger.info(msg)
        if datetime.now().hour > constants.UPDATE_TIME_DAILY_LIMIT:
            # print()
            msg = f'** 开始更新日线数据 [{start_date.strftime(timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)} - {end_date.strftime(timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)}][{adjust}] **'
            logger.info(msg)
            pool = threadpool.ThreadPool(10, q_size=q_size, resq_size=q_size)
            args = [([stock, start_date, end_date, adjust], {}) for stock in stocks]
            requests = threadpool.makeRequests(__init_stock_daily, args)
            [pool.putRequest(req) for req in requests]
            pool.wait()
        else:
            logger.error(f'** 更新时间不能早于 {end_date.strftime(timeutils.DATE_FORMAT_TO_DAY)} {constants.UPDATE_TIME_DAILY_LIMIT} 点')
    else:
        logger.info(f'** 开始更新日线数据 [{start_date.strftime(timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)} - {end_date.strftime(timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)}][{adjust}] **')
        pool = threadpool.ThreadPool(10, q_size=q_size, resq_size=q_size)
        args = [([stock, start_date.strftime(timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH), end_date.strftime(timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH), adjust], {}) for stock in stocks]
        requests = threadpool.makeRequests(__init_stock_daily, args)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        
def update_stock_industry(stock=None):
    if stock == 'all':
        industry_df = __update_stock_industry()
        q_size = len(industry_df.values.tolist())
        pool = threadpool.ThreadPool(10, q_size=q_size, resq_size=q_size)
        args = [([ind_data[1], ind_data[2]], {}) for ind_data in industry_df.values.tolist()]
        requests = threadpool.makeRequests(__update_stock_industry_detail, args)
        [pool.putRequest(req) for req in requests]
        pool.wait()
    else:
        stocks = [stock]

def select_all_stocks():
    return mapper.select_all_code()

# @ttl_cache
def select_stock_daily(stock, fromdate, todate, prepared=False):
    code = stock
    fromdatetime = datetime.strptime(fromdate, timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)
    todatetime = datetime.strptime(todate, timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)
    start_date = fromdatetime.strftime(timeutils.DATE_FORMAT_TO_DAY)
    end_date = todatetime.strftime(timeutils.DATE_FORMAT_TO_DAY)
    if prepared:
        prepared_data = data_cache.get_group(stock)
        # logger.info(f'DATA PREPARED {prepared_data.shape}' )
        return prepared_data
        # return prepared_data.groupby('code').filter(lambda x: (x['code'] == stock).any())
    else:
        return mapper.select_data_between_date(code=code, start_date=start_date, end_date=end_date)

# @ttl_cache(60 * 60 * 2)
def prepare_stock_data(fromdate, todate):
    global data_cache
    if data_cache:
        logger.info(f'FETCHING DATA BY CACHE {data_cache.shape}')
        return data_cache
    logger.info(f"PREPARE DATA {fromdate}-{todate}")
    fromdatetime = datetime.strptime(fromdate, timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)
    todatetime = datetime.strptime(todate, timeutils.DATE_FORMAT_TO_DAY_WITHOUT_DASH)
    # return
    fd = fromdatetime
    day_step = 30
    td = timeutils.get_nextN_day(fromdatetime, day_step)
    data_df = pd.DataFrame()
    data = []
    ft_date_list = [(fd.strftime(timeutils.DATE_FORMAT_TO_DAY), td.strftime(timeutils.DATE_FORMAT_TO_DAY))]
    if timeutils.get_nextN_day(fromdatetime, day_step) > todatetime:
        td = todatetime
        ft_date_list = [(fd.strftime(timeutils.DATE_FORMAT_TO_DAY), td.strftime(timeutils.DATE_FORMAT_TO_DAY))]
    else:
        while td < todatetime:
            fd = timeutils.get_next_day(td)
            td = timeutils.get_nextN_day(fd, day_step)
            if td > todatetime:
                td = todatetime
            start_date = fd.strftime(timeutils.DATE_FORMAT_TO_DAY)
            end_date = td.strftime(timeutils.DATE_FORMAT_TO_DAY)
            ft_date_list.append((start_date, end_date))
    # return mapper.prepare_stock_data(start_date=start_date, end_date=end_date)
    # print(ft_date_list)
    results = []
    pool = threadpool.ThreadPool(20, q_size=len(ft_date_list), resq_size=len(ft_date_list))
    req_args = [([fromdate, todate], {}) for (fromdate, todate) in ft_date_list]
    requests = threadpool.makeRequests(mapper.prepare_stock_data, req_args, callback=lambda x,y: results.append(y))
    [pool.putRequest(req) for req in requests]
    pool.wait()
    for result in results:
        data_df = pd.concat([data_df, result])
    logger.info(f"PREPARE DATA {fromdate}-{todate} Done {data_df.shape}")
    data_cache = data_df.groupby('code')
    return data_df

def concat_df(target_df, source_df):
    print(source_df, target_df)
    source_df = pd.concat([source_df, target_df])

def select_stock_trade_by_date(fromdate=None):
    return mapper.select_stock_trade_by_date(fromdate)

def select_random_stock(stock_num=10):
    stocks = mapper.select_all_code()
    stock_start = random.randint(0, len(stocks) - stock_num - 1)
    stock_end = stock_start + stock_num
    return stocks[stock_start:stock_end]

def select_random_stock_data(fromdate, todate, stock_num=10):
    pass

def get_lastest_trade_date():
    return mapper.get_lastest_trade_date()

def init_stock_info():
    logger.info('** 更新股票基础数据 **')
    df = ak.stock_zh_a_spot()
    df['code'] = df['代码']
    df['symbol'] = df['代码'].map(lambda x: x[2:])
    df['name'] = df['名称']
    stock_df = df[['code', 'symbol', 'name']]
    stock_df.set_index('code', inplace=True)
    # print(stock_df)
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
        logger.info('[UPDATING][%s][%s - %s][%s][%s rows]' % (stock, start_date, end_date, adjust, df['code'].count()))
        base.insert_db(df, constants.STOCK_DAILY_TABLE_NAME, True, "`date`,`code`")
        # else:
            # print('[%s] already exist, pass' % stock)
    except Exception as e:
        traceback.print_exc(e)
        logger.error('error', stock, e)
        
def __update_stock_industry():
    try:
        today = datetime.today().strftime(timeutils.DATE_FORMAT_TO_DAY)
        industry_df = mapper.select_industry_data_by_date(today)
        if not industry_df.empty:
            logger.warning(f'** 股票行业数据 {today} 已更新**')
            return industry_df
        logger.info(f'** 更新股票行业数据 {today} **')
        stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
        stock_board_industry_name_em_df['date'] = today
        stock_board_industry_name_em_df.rename(columns={'排名': 'range'}, inplace=True)
        stock_board_industry_name_em_df.rename(columns={'板块名称': 'ind_name'}, inplace=True)
        stock_board_industry_name_em_df.rename(columns={'板块代码': 'ind_code'}, inplace=True)
        stock_board_industry_name_em_df.rename(columns={'最新价': 'lastest'}, inplace=True)
        stock_board_industry_name_em_df.rename(columns={'涨跌额': 'inc'}, inplace=True)
        stock_board_industry_name_em_df.rename(columns={'涨跌幅': 'inc_rate'}, inplace=True)
        stock_board_industry_name_em_df.rename(columns={'总市值': 'total'}, inplace=True)
        stock_board_industry_name_em_df.rename(columns={'换手率': 'turnover'}, inplace=True)
        stock_board_industry_name_em_df.rename(columns={'上涨家数': 'rise'}, inplace=True)
        stock_board_industry_name_em_df.rename(columns={'下跌家数': 'fall'}, inplace=True)
        stock_board_industry_name_em_df.rename(columns={'领涨股票': 'leading_stock'}, inplace=True)
        stock_board_industry_name_em_df.rename(columns={'领涨股票-涨跌幅': 'leading_stock_inc'}, inplace=True)
        stock_board_industry_name_em_df.set_index('range', inplace=True)
        base.insert_db(stock_board_industry_name_em_df, constants.STOCK_INDUSTRY_TABLE_NAME, True, "`date`,`range`,`ind_code`")
        return stock_board_industry_name_em_df
    except Exception as e:
        traceback.print_exc(e)
        logger.error('update industry error', e)
        
def __update_stock_industry_detail(industry_name, indusctry_code):
    try:
        today = datetime.today().strftime(timeutils.DATE_FORMAT_TO_DAY)
        industry_df = mapper.select_industry_data_detail(indusctry_code, today)
        if not industry_df.empty:
            logger.warning(f'** 股票行业明细数据 {today} 已更新**')
            return
        logger.info(f'** 更新股票行业明细数据 {today} **')
        stock_board_industry_cons_em_df = ak.stock_board_industry_cons_em(symbol=industry_name)
        stock_board_industry_cons_em_df['ind_name'] = industry_name
        stock_board_industry_cons_em_df['ind_code'] = indusctry_code
        stock_board_industry_cons_em_df.rename(columns={'代码': 'symbol'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'名称': 'symbol_name'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'最新价': 'price_now'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'涨跌幅': 'inc_rate'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'涨跌额': 'inc'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'成交量': 'volume'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'成交额': 'money'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'振幅': 'amplitude'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'最高': 'high'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'最低': 'low'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'今开': 'open'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'昨收': 'close'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'换手率': 'turnover'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'市盈率-动态': 'PE'}, inplace=True)
        stock_board_industry_cons_em_df.rename(columns={'市净率': 'PB'}, inplace=True)
        stock_board_industry_cons_em_df['序号'] = today
        stock_board_industry_cons_em_df.rename(columns={'序号': 'date'}, inplace=True)
        stock_board_industry_cons_em_df.set_index('symbol', inplace=True)
        base.insert_db(stock_board_industry_cons_em_df, constants.STOCK_INDUSTRY_DETAIL_TABLE_NAME, True, "`date`,`symbol`,`ind_code`")
    except Exception as e:
        traceback.print_exc(e)
        logger.error('update stock industry detail error', e)
        
if __name__ == '__main__':
    # update_stock_daily()
    __update_stock_industry()