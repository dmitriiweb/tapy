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


def calculate_smma(df, period, column_name, apply_to):
    """Calculate Smoothed Moving Average"""
    # TODO Need improve
    prices = df[apply_to].tolist()
    smma_vals = []

    # First value for SMMA
    first_val = df[apply_to].iloc[:period].mean()
    smma_vals.append(first_val)

    # Calculate SMMA
    for i in range(1, len(prices), 1):
        try:
            smma_val = (smma_vals[i-1] * (period-1) + prices[i+period]) / period
            smma_vals.append(smma_val)
        except IndexError:
            break

    df = pd.DataFrame(smma_vals, columns=[column_name])
    return df

