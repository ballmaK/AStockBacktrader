#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import argparse
import datetime
import pandas as pd
import backtrader as bt
from pandas import DataFrame as DF
from data.db import common, base, constants
from utils import threadpool, timeutils
from bt.strategies.lightvolume import LightVolume
from utils.datautils import df_convert
from utils.timeutils import *
from message.bot import *

def run(code, args, fromdate, todate):
    try:
        # filter bj market
        exe_date = datetime.datetime.now().strftime(timeutils.DATE_FORMAT_TO_DAY)
        if 'bj' in code or 'sh688' in code:
            return
        # Create a cerebro
        cerebro = bt.Cerebro()

        # Get the dates from the args
        
        data = common.select_stock_daily(stock=code, fromdate=fromdate.strftime(DATE_FORMAT_TO_DAY_WITHOUT_DASH), todate=todate.strftime(DATE_FORMAT_TO_DAY_WITHOUT_DASH))
        cerebro.adddata(data=bt.feeds.PandasData(dataname=df_convert(data), fromdate=fromdate, todate=todate))
        
        # Add the strategy
        cerebro.addstrategy(LightVolume)
        
        cerebro.addanalyzer(bt.analyzers.SharpeRatio)
        cerebro.addanalyzer(bt.analyzers.Returns)
        cerebro.addanalyzer(bt.analyzers.VWR)
        
        cerebro.addsizer(bt.sizers.PercentSizer, percents=90)

        # Add the commission - only stocks like a for each operation
        cerebro.broker.setcash(args.cash)

        # Add the commission - only stocks like a for each operation
        cerebro.broker.setcommission(commission=args.commperc)

        # And run it
        
        # ret = cerebro.run(runonce=not args.runnext,
        #             preload=not args.nopreload,
        #             oldsync=args.oldsync)
        ret = cerebro.run()
        if ret:
            strats = [ strat for i, strat in enumerate(ret)]
            # print('Sharpe Ratio:', strats[0].analyzers.sharperatio.get_analysis())
            # print('Returns: ', strats[0].analyzers.returns.get_analysis())
            # print('VWR: ', strats[0].analyzers.vwr.get_analysis())
            sharpe = strats[0].analyzers.sharperatio.get_analysis()['sharperatio']
            rnorm100 = strats[0].analyzers.returns.get_analysis()['rnorm100']
            # print(sharpe, rnorm100)
            if len(strats[0].orders) >= 1:
                last_order_date = strats[0].orders[-1]['datetime']
                last_order_type = strats[0].orders[-1]['side']
                last_order_price = strats[0].orders[-1]['price']
                last_order_price_now = strats[0].orders[-1]['price_now']
                # print(f"{exe_date},{code},{sharpe},{rnorm100},{last_order_date},{last_order_type},{last_order_price},{last_order_price_now}")
                # if last_order_date == today and last_order_type == 'BUY':
                return ((exe_date),(code),(sharpe),(rnorm100),(last_order_date),(last_order_type),(last_order_price),(last_order_price_now))
            # trade_df = DF.from_records(strats[0].orders)
            # print(trade_df)
    except Exception as e:
        print(f'{code} select error')
        
def handle_results(request, result):
    if result:
        return result

def runstrategy():
    args = parse_args()
    
    fromdate = datetime.datetime.strptime(args.fromdate, '%Y%m%d')
    if not args.todate:
        todate  = common.get_lastest_trade_date().replace('-', '')
        todate = datetime.datetime.strptime(todate, '%Y%m%d')
    else:
        todate = datetime.datetime.strptime(args.todate, '%Y%m%d')
    if args.stock_num == 'all':
        codes = common.select_all_stocks()
    else:
        codes = common.select_random_stock(int(args.stock_num))

    results = []
    pool = threadpool.ThreadPool(20, q_size=len(codes), resq_size=len(codes))
    req_args = [([stock, args, fromdate, todate], {}) for stock in codes]
    requests = threadpool.makeRequests(run, req_args, callback=lambda x,y: results.append(y))
    [pool.putRequest(req) for req in requests]
    pool.wait()
    # print(results)
    # for code in codes:
    #     results.append(run(code, args, fromdate, todate))
    # else:
    df = pd.DataFrame([ result for result in results if result is not None], 
                    #   index=['exe_date'],
                      columns=['exe_date','code', 'sharpe', 'rnorm100','last_order_date','last_order_type','last_order_price','last_order_price_now'])
    df['last_order_date'] = df['last_order_date'].map(timeutils.reformat_date)
    df.set_index(['exe_date'], inplace=True)
    # df.to_csv(f"select_results/{datetime.datetime.today().strftime(DATE_FORMAT_TO_DAY)}-{datetime.datetime.now().microsecond}.csv", header=True)
    bot = QYWXMessageBot(WEB_HOOK)
    if not df.empty:
        send_message(bot, df)
        base.insert_db(df, constants.STOCK_DAILY_RESULT_TABLE_NAME, True, "`exe_date`,`code`,`last_order_date`,`last_order_type`")
    else:
        message = str.format(f'【{datetime.datetime.today().strftime(timeutils.DATE_FORMAT_TO_DAY)}】今日无推荐')
        bot.send_message(message)
    
def send_message(bot, df):
    buy_df = df.loc[df['last_order_type'] == 'BUY', ['code', 'rnorm100','last_order_date','last_order_type']]
    sell_df = df.loc[df['last_order_type'] == 'SELL', ['code', 'rnorm100','last_order_date','last_order_type']]
    # filtered_df = df.loc[(df['age'] > 25) & (df['gender'] == 'M'), ['code', 'rnorm100','last_order_date','last_order_type']]
    buy_message = str.format(
        f'<font color="warning"># 【{datetime.datetime.today().strftime(timeutils.DATE_FORMAT_TO_DAY)}】推荐买入</font>\n')
    for row in df.itertuples(index=False):
        msg_row = str.format(f'#### {row.code}, 模拟年化：{row.rnorm100}\n')
        buy_message = buy_message + msg_row
    message = QYWXMessageMD(buy_message)
    bot.send_message(message)
    


def parse_args():
    parser = argparse.ArgumentParser(description='Select Stock Script')

    parser.add_argument('--fromdate', '-f',
                        default='20220101', required=True,
                        help='Starting date in YYYYMMDD format')

    parser.add_argument('--todate', '-t',
                        help='Starting date in YYYYMMDD format')

    parser.add_argument('--period', default=45, type=int,
                        help='Period to apply to the LightVolume')

    parser.add_argument('--cash', default=100000, type=int, required=True,
                        help='Starting Cash')
    
    parser.add_argument('--stock-num', default='10',
                        help='Stock pool number')

    parser.add_argument('--runnext', action='store_true',
                        help='Use next by next instead of runonce')

    parser.add_argument('--nopreload', action='store_true',
                        help='Do not preload the data')

    parser.add_argument('--oldsync', action='store_true',
                        help='Use old data synchronization method')

    parser.add_argument('--commperc', default=0.001, type=float,
                        help='Percentage commission (0.005 is 0.5%%')

    parser.add_argument('--numfigs', '-n', default=1,
                        help='Plot using numfigs figures')

    return parser.parse_args()


if __name__ == '__main__':
    runstrategy()