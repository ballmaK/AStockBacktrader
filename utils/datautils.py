
import pandas as pd
def df_convert(df):
    df['open'] = pd.to_numeric(df['open'])
    df['close'] = pd.to_numeric(df['close'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['volume'] = pd.to_numeric(df['volume'])
    df = df.sort_values(by=['date'], ascending=True)
    df.index = pd.to_datetime(df['date'])
    return df