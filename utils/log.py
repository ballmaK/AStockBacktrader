# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger("astockbacktrader")
logger.setLevel(logging.INFO)
logfile = 'logs/astockbacktrader.log'
fh = logging.FileHandler(logfile, mode='a')

logger.propagate = False

fmt = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(filename)s %(lineno)s: %(message)s"
)
ch = logging.StreamHandler()

ch.setFormatter(fmt)
fh.setFormatter(fmt)
logger.handlers.append(ch)
logger.handlers.append(fh)