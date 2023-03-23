#!/usr/bin/env python
# -*- coding: utf-8;

import argparse

import backtrader as bt
import backtrader.btrun as btrun

from backtrader.btrun.btrun import parse_args as bt_parse_args

def run(pargs=''):
    # btrun.btrun(pargs)
    args = parse_args(pargs)
    btargs = bt_parse_args(pargs)
    args_merged = argparse.Namespace(**vars(args), **vars(btargs))
    # print(btargs, args)


def parse_args(pargs=''):
    parser = argparse.ArgumentParser(
        description='Run Script',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    
    # add data options
    group = parser.add_argument_group(title='Data options')
    
    group.add_argument('--update-daily', '-u', required=False,
                       dest='update_daily',
                       help='Update daily data')
    
    group.add_argument('--reupdate-daily', '-ru', required=False,
                       dest='reupdate_daily',
                       help='Reupdate daily data')
    
    group.add_argument('--startdate', '-sd', required=False, default=None,
                       help='Starting date in YYYY-MM-DD format')

    group.add_argument('--enddate', '-ed', required=False, default=None,
                       help='Ending date in YYYY-MM-DD format')
    
    return parser.parse_args()
    

if __name__ == '__main__':
    run()