#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import easytrader
import pandas as pd
from utils.log import logger
LOGON_COOKIE = os.environ.get('LOGON_COOKIE') if (os.environ.get('LOGON_COOKIE') != None) else "logon_cookie"

def load_user():
    user = easytrader.use('xq')
    user.prepare("./real_trade/xq_config.json")
    return user

def adjust_weight(trade_df=None, user=None):
    if not user:
        return
    user_position = user.position
    user_balance = user.balance
    position_df = pd.DataFrame(user_position)
    print("持仓数据: ")
    print(position_df)
    balance_df = pd.DataFrame(user_balance)
    print("余额数据: ")
    print(balance_df)
    # result = list(filter(lambda x: (x['stock_code'] == symbol.upper()), user.position)) 
    for stock in trade_df.itertuples():
        # print(stock)
        # 判断是否持仓该股
        if not position_df.groupby('stock_code').filter(lambda x: x['stock_code'] == stock.code.upper()).empty:
            print(f'[持仓] {stock.name}({stock.code})')
        else:
            # 买 or 卖
            if stock.sell_date != '--':
                # 买
                # print(f'[开仓] {stock.name} {stock.code}, {2}')
                user.adjust_weight(stock.code[2:], 0)
            else:
                # 卖
                # print(f'[平仓] {stock.name} {stock.code}')
                user.adjust_weight(stock.code[2:], 2)
    # if not len(result) and weight > 0:
    #     print(f'[ADJUST_WEIGHT] BUY {symbol}, {weight}')
    #     user.adjust_weight(symbol[2:], weight)
    # elif len(result) > 0 and weight == 0:
    #     print(f'[ADJUST_WEIGHT] SELL {symbol}')
    #     user.adjust_weight(symbol[2:], weight)
    # else:
    #     print(f'[ADJUST_WEIGHT] Ignore {symbol}')
