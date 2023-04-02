#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import argparse
import datetime
import pandas as pd
import backtrader as bt
from data.db import common
from bt.strategies.lightvolume import LightVolume
from utils.datautils import df_convert
from utils.timeutils import *

def runstrategy():
    args = parse_args()
    
    fromdate = datetime.datetime.strptime(args.fromdate, '%Y%m%d')
    if not args.todate:
        todate  = common.get_lastest_trade_date().replace('-', '')
    else:
        todate = datetime.datetime.strptime(args.todate, '%Y%m%d')
    
    if args.stock_num == 'all':
        codes = common.select_all_stocks()
    else:
        codes = common.select_random_stock(int(args.stock_num))

    results = []
    for code in codes:
        # Create a cerebro
        cerebro = bt.Cerebro()

        # Get the dates from the args
        
        data = common.select_stock_daily(stock=code, fromdate=fromdate.strftime(DATE_FORMAT_TO_DAY_WITHOUT_DASH), todate=todate.strftime(DATE_FORMAT_TO_DAY_WITHOUT_DASH))
        
        cerebro.adddata(data=bt.feeds.PandasData(dataname=df_convert(data), fromdate=fromdate, todate=todate))
        
        # Add the strategy
        cerebro.addstrategy(LightVolume)
        
        cerebro.addanalyzer(bt.analyzers.SharpeRatio)
        cerebro.addanalyzer(bt.analyzers.Returns)

        # Add the commission - only stocks like a for each operation
        cerebro.broker.setcash(args.cash)

        # Add the commission - only stocks like a for each operation
        cerebro.broker.setcommission(commission=args.commperc)

        # And run it
        
        ret = cerebro.run(runonce=not args.runnext,
                    preload=not args.nopreload,
                    oldsync=args.oldsync)
        if ret:
            strats = [ strat for i, strat in enumerate(ret)]
            # print(dir(strats[0]))
            # print(strats[0].orders[-1])
            sharpe = strats[0].analyzers.sharperatio.get_analysis()['sharperatio']
            rnorm100 = strats[0].analyzers.returns.get_analysis()['rnorm100']
            if len(strats[0].orders) >= 1:
                last_order_date = strats[0].orders[-1]['datetime']
                last_order_type = strats[0].orders[-1]['side']
                last_order_price = strats[0].orders[-1]['price']
                last_order_price_now = strats[0].orders[-1]['price_now']
                today = datetime.datetime.strptime(common.get_lastest_trade_date(), "%Y-%m-%d")
                print(f"{code},{sharpe},{rnorm100},{last_order_date},{last_order_type},{last_order_price},{last_order_price_now}")
                # if last_order_date == today and last_order_type == 'BUY':
                results.append(((code),(sharpe),(rnorm100),(last_order_date),(last_order_type),(last_order_price),(last_order_price_now)))
    else:
        df = pd.DataFrame(results, columns=['code', 'sharpe', 'rnorm100','last_order_date','last_order_type','last_order_price','last_order_price_now'])
        df.to_csv(f"select_results/{datetime.datetime.today().strftime(DATE_FORMAT_TO_DAY)}-{datetime.datetime.now().microsecond}.csv", header=True)
    

    


def parse_args():
    parser = argparse.ArgumentParser(description='Select Stock Script')

    parser.add_argument('--fromdate', '-f',
                        default='20220101', required=True,
                        help='Starting date in YYYYMMDD format')

    parser.add_argument('--todate', '-t',
                        default='20230324', 
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