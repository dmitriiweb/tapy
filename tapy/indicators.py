import pandas as pd

from .utils import calculate_ao, calculate_sma

__version__ = '1.0.1'


class Indicators:
    """
    Add technical indicators data to a pandas data frame

    Example:
    ~~~~~~~~
        >>> import pandas as pd
        >>> from tapy import Indicators
        >>> df = pd.read_csv('EURUSD60.csv')
        >>> indicators = Indicators(df)
        >>> indicators.sma(period=3, column_name='SMA_3')
        >>> df.tail()
              Date   Time     Open     High      Low    Close  Volume     SMA_3
        2019.09.20  16:00  1.10022  1.10105  1.10010  1.10070    2888  1.100667
        2019.09.20  17:00  1.10068  1.10193  1.10054  1.10184    6116  1.100920
        2019.09.20  18:00  1.10186  1.10194  1.10095  1.10144    3757  1.101327
        2019.09.20  19:00  1.10146  1.10215  1.10121  1.10188    3069  1.101720
        2019.09.20  20:00  1.10184  1.10215  1.10147  1.10167    1224  1.101663
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
        self.columns = {
            'Open': open_col,
            'High': high_col,
            'Low': low_col,
            'Close': close_col,
            'Volume': volume_col
        }

    def sma(self, period=5, column_name='sma', apply_to='Close'):
        """
        Simple Moving Average (SMA)
        ---------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/moving_average#simple_moving_average

            >>> indicators.sma(period=5, column_name='sma', apply_to='Close')

            :param int period: the number of calculation periods, default: 5
            :param str column_name: Column name, default: sma
            :param str apply_to: Which column use for calculation.
                Can be *"Open"*, *"High"*, *"Low"* and *"Close"*.
                **Default**: Close
            :return: None

        """
        calculate_sma(self.df, period, column_name, apply_to)

    def ema(self, period=5, column_name='ema', apply_to='Close'):
        """
        Exponential Moving Average (EMA)
        ---------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/moving_average#exponential_moving_average

            >>> indicators.ema(period=5, column_name='ema', apply_to='Close')

            :param int period: the number of calculation periods, default: 5
            :param str column_name: Column name, default: ema
            :param str apply_to: Which column use for calculation.
                Can be *"Open"*, *"High"*, *"Low"* and *"Close"*.
                **Default**: Close
            :return: None

        """
        self.df[column_name] = self.df[self.columns[apply_to]].ewm(span=period, adjust=False).mean()

    def awesome_oscillator(self, column_name='ao'):
        """
        Awesome Oscillator (AO)
        -----------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/awesome_oscillator

            >>> indicators.awesome_oscillator(column_name='ao')

            :param str column_name: Column name, default: ao
            :return: None
        """
        # Data frame for storing temporary data
        df_tmp = pd.DataFrame()
        df_tmp['High'] = self.df[self.columns['High']]
        df_tmp['Low'] = self.df[self.columns['Low']]

        # Calculate Awesome Oscillator
        calculate_ao(df_tmp, 'ao')
        self.df[column_name] = df_tmp['ao']

    def accelerator_oscillator(self, column_name='ac'):
        """
        Accelerator Oscillator (AC)
        -----------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/accelerator_decelerator

            >>> indicators.accelerator_oscillator(column_name='ac')

            :param str column_name: Column name, default: ac
            :return: None
        """
        pass
        # Data frame for storing temporary data
        df_tmp = pd.DataFrame()
        df_tmp['High'] = self.df[self.columns['High']]
        df_tmp['Low'] = self.df[self.columns['Low']]

        # Calculate Awesome Oscillator
        calculate_ao(df_tmp, 'ao')

        # Calculate SMA for Awesome Oscillator
        calculate_sma(df_tmp, 5, 'sma_ao', 'ao')

        # Calculate Accelerator Oscillator
        self.df[column_name] = df_tmp['ao'] - df_tmp['sma_ao']

    def accumulation_distribution(self, column_name='a/d'):
        """
        Accumulation/Distribution (A/D)
        ---------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/accumulation_distribution

            >>> indicators.accumulation_distribution(column_name='a/d')

            :param str column_name: Column name, default: a/d
            :return: None

        """
        # Temporary df
        df_tmp = pd.DataFrame()
        df_tmp['close'] = self.df[self.columns['Close']]
        df_tmp['high'] = self.df[self.columns['High']]
        df_tmp['low'] = self.df[self.columns['Low']]
        df_tmp['volume'] = self.df[self.columns['Volume']]

        df_tmp['calc'] = (
                                 (df_tmp['close'] - df_tmp['low']) - (df_tmp['high'] - df_tmp['close'])
                         ) * df_tmp['volume'] / (df_tmp['high'] - df_tmp['low'])

        self.df[column_name] = df_tmp['calc'].explode().sum()
