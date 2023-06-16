#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import easytrader
LOGON_COOKIE = os.environ.get('LOGON_COOKIE') if (os.environ.get('LOGON_COOKIE') != None) else "logon_cookie"

user = easytrader.use('xq')

if __name__ == '__main__':
    user.prepare("xq_config.json")
    print(user.position)