import backtrader as bt
import pyfolio as pf
import pandas as pd
from datetime import datetime
from backtrader.utils.py3 import iteritems
from pandas import DataFrame as DF
def strat_ret_handler(cerebro, strat):
    # Results of own analyzers
    for i, a in enumerate(strat.analyzers):
        if isinstance(a, bt.analyzers.PyFolio):
            returns, positions, transactions, gross_lev = a.get_pf_items()
            print('-- RETURNS')
            print(returns)
            print('-- POSITIONS')
            print(positions)
            print('-- TRANSACTIONS')
            print(transactions)
            print('-- GROSS LEVERAGE')
            print(gross_lev)
            pf.create_full_tear_sheet(
                returns,
                positions=positions,
                transactions=transactions,
                estimate_intraday=False,
                live_start_date='2022-09-21',
                round_trips=True)
            # cerebro.plot()
        else:
            df = DF.from_records(iteritems(a.get_analysis()))
            # print(df)
            results = []
            sharpe = strat.analyzers.sharperatio.get_analysis()['sharperatio']
            rnorm100 = strat.analyzers.returns.get_analysis()['rnorm100']
            if len(strat.orders) >= 1:
                last_order_date = strat.orders[-1]['datetime']
                last_order_type = strat.orders[-1]['side']
                last_order_price = strat.orders[-1]['price']
                last_order_price_now = strat.orders[-1]['price_now']
                # today = datetime.strptime(getMaxTradeDate(), "%Y-%m-%d")
                code = strat.orders[-1]['stock']
                print(f"{code},{sharpe},{rnorm100},{last_order_date},{last_order_type},{last_order_price},{last_order_price_now}")
                results.append(((code),(sharpe),(rnorm100)))
                if last_order_type == 'BUY': # last_order_date == today and 
                    df = pd.DataFrame(results, columns=['code', 'sharpe', 'rnorm100'])
                    print(df)
    else:
        trade_df = DF.from_records(strat.orders)
        print(trade_df)
            

            