__version__ = '1.0.0'


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
    def __init__(
            self,
            df,
            open_col='Open',
            high_col='High',
            low_col='Low',
            close_col='Close',
            volume_col='Volume'
    ):
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
        :param int period: the number of calculation periods, default: 5
        :param str column_name: Column name, default: sma
        :return: None

        Example:
        ~~~~~~~~
            >>> import pandas as pd
            >>> from tapy import Indicators
            >>> df = pd.read_csv('EURUSD60.csv')
            >>> indicators = Indicators(df)
            >>> indicators.sma(period=3, column_name='SMA')
            Date   Time     Open     High      Low    Close  Volume       SMA
            3723  2019.09.20  16:00  1.10022  1.10105  1.10010  1.10070    2888  1.100667
            3724  2019.09.20  17:00  1.10068  1.10193  1.10054  1.10184    6116  1.100920
            3725  2019.09.20  18:00  1.10186  1.10194  1.10095  1.10144    3757  1.101327
            3726  2019.09.20  19:00  1.10146  1.10215  1.10121  1.10188    3069  1.101720
            3727  2019.09.20  20:00  1.10184  1.10215  1.10147  1.10167    1224  1.101663
        """
        self.df[column_name] = self.df[self.close_col].rolling(window=period).mean()
        print(self.df.tail())
