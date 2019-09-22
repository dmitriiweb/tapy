__version__ = '0.0.0b'


class Indicators:
    """
    Add technical indicators data to a pandas data frame

    Example:
    ~~~~~~~~
        >>> import pandas as pd
        >>> from tapy import Indicators
        >>> df = pd.read_csv('EURUSD60.csv')
        >>> indicators = Indicators(df)
    """
    def __init__(self, df, open_col='Open', high_col='High', low_col='Low', close_col='Close', volume_col='Volume'):
        """
        Initiate Indicators object

        :param pandas data frame df: Should contain OHLC columns and Volume column
        :param str open_col: Name of Open column in df
        :param str high_col: Name of High column in df
        :param str low_col: Name of Low column in df
        :param str close_col: Name of Close column in df
        :param str volume_col: Name of Volume column in df. This column is optional
            and require only if indicator use this data.
        """
        self.df = df
        self.open_col = open_col
        self.high_col = high_col
        self.low_col = low_col
        self.close_col = close_col
        self.volume_col = volume_col

    def sma(self, period=5, column_name='sma'):
        """
        Simple Moving Average
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/moving_average#simple_moving_average
        :param int period: the number of calculation periods
        :param str column_name: Column name
        :return: None

        Example:
        ~~~~~~~~
        """
        self.df[column_name] = self.df[self.close_col].rolling(window=period).mean()
        print(self.df.tail())
