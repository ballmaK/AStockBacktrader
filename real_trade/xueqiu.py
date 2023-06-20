#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import easytrader
LOGON_COOKIE = os.environ.get('LOGON_COOKIE') if (os.environ.get('LOGON_COOKIE') != None) else "logon_cookie"

def adjust_weight(symbol=None, weight=None):
    user = easytrader.use('xq')
    user.prepare("xq_config.json")
    user.adjust_weight(symbol, weight)
