#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import easytrader
LOGON_COOKIE = os.environ.get('LOGON_COOKIE') if (os.environ.get('LOGON_COOKIE') != None) else "logon_cookie"

def load_user():
    user = easytrader.use('xq')
    user.prepare("./real_trade/xq_config.json")
    return user

def adjust_weight(symbol=None, weight=None, user=None):
    if not user:
        return
    print(user.position)
    print(user.balance)
    result = list(filter(lambda x: (x['stock_code'] == symbol.upper()), user.position)) 
    if not len(result) and weight > 0:
        print(f'[ADJUST_WEIGHT] BUY {symbol}, {weight}')
        user.adjust_weight(symbol[2:], weight)
    elif len(result) > 0 and weight == 0:
        print(f'[ADJUST_WEIGHT] SELL {symbol}')
        user.adjust_weight(symbol[2:], weight)
    else:
        print(f'[ADJUST_WEIGHT] Ignore {symbol}')
