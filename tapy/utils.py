import pandas as pd


def calculate_sma(df, period, column_name, apply_to):
    """Calculate Simple Moving Averaga"""
    df[column_name] = df[apply_to].rolling(window=period).mean()


def calculate_ao(df, column_name):
    """Calculate Awesome Oscillator"""
    # Data frame for storing temporary data
    df_tmp = pd.DataFrame()

    mp_col = '_median_price'
    df_tmp[mp_col] = (df['High'] + df['Low']) / 2

    sma5_col = '_sma5'
    calculate_sma(df_tmp, 5, sma5_col, mp_col)

    sma34_col = '_sma34'
    calculate_sma(df_tmp, 34, sma34_col, mp_col)

    # Calculate Awesome Oscillator
    df[column_name] = df_tmp[sma5_col] - df_tmp[sma34_col]
