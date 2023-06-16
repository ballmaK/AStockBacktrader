#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import easytrader
LOGON_COOKIE = os.environ.get('LOGON_COOKIE') if (os.environ.get('LOGON_COOKIE') != None) else "logon_cookie"

user = easytrader.use('xq')

context = {
  "cookies": LOGON_COOKIE,
  "portfolio_code": "ZH3239610",
  "portfolio_market": "cn"
}

if __name__ == '__main__':
    user.prepare(config_file=None, **context)
    print(user.position)