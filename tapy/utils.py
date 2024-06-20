import pandas as pd
import numpy as np
from numpy import mean, absolute


def calculate_sma(df, period, column_name, apply_to):
    """Calculate Simple Moving Averaga."""
    df[column_name] = df[apply_to].rolling(window=period).mean()


def calculate_ao(df, column_name):
    """Calculate Awesome Oscillator."""
    # Data frame for storing temporary data
    df_tmp = pd.DataFrame()

    mp_col = "_median_price"
    df_tmp[mp_col] = (df["High"] + df["Low"]) / 2

    sma5_col = "_sma5"
    calculate_sma(df_tmp, 5, sma5_col, mp_col)

    sma34_col = "_sma34"
    calculate_sma(df_tmp, 34, sma34_col, mp_col)

    # Calculate Awesome Oscillator
    df[column_name] = df_tmp[sma5_col] - df_tmp[sma34_col]


def calculate_smma(df, period, column_name, apply_to):
    """Calculate Smoothed Moving Average."""
    df_tmp = df[[apply_to]]
    first_val = df_tmp[apply_to].iloc[:period].mean()
    df_tmp = df_tmp.assign(column_name=None)
    df_tmp.at[period, column_name] = first_val
    for index, row in df_tmp.iterrows():
        if index > period:
            smma_val = (
                df_tmp.at[index - 1, column_name] * (period - 1)
                + row[apply_to]
            ) / period
            df_tmp.at[index, column_name] = smma_val
    df_tmp = df_tmp[[column_name]]
    return df_tmp


def mad(data, axis=None):
    """Calculate Average absolute deviation."""
    return mean(absolute(data - mean(data, axis)), axis)


def calculate_alma(df, period, offset, sigma, apply_to, column_name):
    m = offset * (period - 1)
    s = period / sigma

    # Gaussian distribution weight calculation
    weights = np.exp(-((np.arange(period) - m) ** 2) / (2 * s * s))
    weights /= np.sum(weights)

    # Apply the weights to the specified column
    alma = (
        df[apply_to]
        .rolling(window=period)
        .apply(lambda x: np.sum(weights * x), raw=True)
    )

    df[column_name] = alma
    return df
