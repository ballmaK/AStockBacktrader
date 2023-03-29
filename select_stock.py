#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import argparse
import datetime
import pandas as pd
import backtrader as bt
from .data.db import common
from bt.strategies.lightvolume import LightVolume

def runstrategy():
    args = parse_args()
    
    codes = common.select_all_stocks()
    end_date  = common.get_lastest_trade_date().replace('-', '')
    start_cash = 100000
    total_cash = 0
    current_cash = 0
    results = []
    for code in codes:
        total_cash = total_cash + start_cash
        # Create a cerebro
        cerebro = bt.Cerebro()

        # Get the dates from the args
        fromdate = datetime.datetime.strptime(args.fromdate, '%Y%m%d')
        todate = datetime.datetime.strptime(args.todate, '%Y%m%d')
        
        cerebro
        # Add the strategy
        cerebro.addstrategy(LightVolume,
                            period=args.period,
                            stake=args.stake)

        # Add the commission - only stocks like a for each operation
        cerebro.broker.setcash(args.cash)

        # Add the commission - only stocks like a for each operation
        cerebro.broker.setcommission(commission=args.commperc)

        # And run it
        
        ret = cerebro.run(runonce=not args.runnext,
                    preload=not args.nopreload,
                    oldsync=args.oldsync)
        if cerebro:
            results.append(cerebro)
    else:
        df = pd.DataFrame(results, columns=['code', 'sharpe', 'rnorm100'])
        print(df)

    

    


def parse_args():
    parser = argparse.ArgumentParser(description='Select Stock Script')

    parser.add_argument('--fromdate', '-f',
                        default='20220101',
                        help='Starting date in YYYYMMDD format')

    parser.add_argument('--todate', '-t',
                        default='20230324',
                        help='Starting date in YYYYMMDD format')

    parser.add_argument('--period', default=45, type=int,
                        help='Period to apply to the LightVolume')

    parser.add_argument('--cash', default=100000, type=int,
                        help='Starting Cash')

    parser.add_argument('--runnext', action='store_true',
                        help='Use next by next instead of runonce')

    parser.add_argument('--nopreload', action='store_true',
                        help='Do not preload the data')

    parser.add_argument('--oldsync', action='store_true',
                        help='Use old data synchronization method')

    parser.add_argument('--commperc', default=0.005, type=float,
                        help='Percentage commission (0.005 is 0.5%%')

    parser.add_argument('--numfigs', '-n', default=1,
                        help='Plot using numfigs figures')

    return parser.parse_args()


if __name__ == '__main__':
    runstrategy()