STOCK_BASE_TABLE_NAME = 'stock_base'
STOCK_DAILY_TABLE_NAME = 'stock_daily'
STOCK_DAILY_RESULT_TABLE_NAME = 'stock_daily_result'
STOCK_TRADE_LOG_TABLE_NAME = 'stock_trade_log'
STOCK_TRADE_POLICY_RESULT_TABLE_NAME = 'stock_trade_policy_result'

ASHARE_MARKET = dict(
    sh='sh',
    sz='sz',
    bj='bj'
)

# 每日数据更新时间限制，不能早于该时间点更新每日数据
UPDATE_TIME_DAILY_LIMIT = 16