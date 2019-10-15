import pandas as pd
import numpy as np

from .utils import calculate_ao, calculate_sma, calculate_smma, mad

__version__ = '1.6.0'


class Indicators:
    """
    Add technical indicators data to a pandas data frame

    Example:
    ~~~~~~~~
        >>> import pandas as pd
        >>> from tapy import Indicators
        >>> df = pd.read_csv('EURUSD60.csv')
        >>> indicators = Indicators(df)
        >>> indicators.accelerator_oscillator(column_name='AC')
        >>> indicators.sma()
        >>> df = indicators.df
        >>> df.tail()
                    Date   Time     Open     High      Low    Close  Volume        AC       sma
        3723  2019.09.20  16:00  1.10022  1.10105  1.10010  1.10070    2888 -0.001155  1.101296
        3724  2019.09.20  17:00  1.10068  1.10193  1.10054  1.10184    6116 -0.000820  1.101158
        3725  2019.09.20  18:00  1.10186  1.10194  1.10095  1.10144    3757 -0.000400  1.101056
        3726  2019.09.20  19:00  1.10146  1.10215  1.10121  1.10188    3069  0.000022  1.101216
        3727  2019.09.20  20:00  1.10184  1.10215  1.10147  1.10167    1224  0.000388  1.101506
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
        self._columns = {
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

            >>> Indicators.sma(period=5, column_name='sma', apply_to='Close')

            :param int period: the number of calculation periods, default: 5
            :param str column_name: Column name, default: sma
            :param str apply_to: Which column use for calculation.
                Can be *"Open"*, *"High"*, *"Low"* and *"Close"*.
                **Default**: Close
            :return: None

        """
        calculate_sma(self.df, period, column_name, apply_to)

    def smma(self, period=5, column_name='smma', apply_to='Close'):
        """
        Smoothed Moving Average (SMMA)
        ---------------------
            https://www.metatrader4.com/ru/trading-platform/help/analytics/tech_indicators/moving_average#smoothed_moving_average

            >>> Indicators.smma(period=5, column_name='smma', apply_to='Close')

            :param int period: the number of calculation periods, default: 5
            :param str column_name: Column name, default: smma
            :param str apply_to: Which column use for calculation.
                Can be *"Open"*, *"High"*, *"Low"* and *"Close"*.
                **Default**: Close
            :return: None

        """
        df_smma = calculate_smma(self.df, period, column_name, apply_to)
        self.df = self.df.merge(df_smma, left_index=True, right_index=True)

    def ema(self, period=5, column_name='ema', apply_to='Close'):
        """
        Exponential Moving Average (EMA)
        ---------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/moving_average#exponential_moving_average

            >>> Indicators.ema(period=5, column_name='ema', apply_to='Close')

            :param int period: the number of calculation periods, default: 5
            :param str column_name: Column name, default: ema
            :param str apply_to: Which column use for calculation.
                Can be *"Open"*, *"High"*, *"Low"* and *"Close"*.
                **Default**: Close
            :return: None

        """
        self.df[column_name] = self.df[self._columns[apply_to]].ewm(
            span=period, adjust=False).mean()

    def awesome_oscillator(self, column_name='ao'):
        """
        Awesome Oscillator (AO)
        -----------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/awesome_oscillator

            >>> Indicators.awesome_oscillator(column_name='ao')

            :param str column_name: Column name, default: ao
            :return: None
        """
        # Data frame for storing temporary data
        df_tmp = pd.DataFrame()
        df_tmp['High'] = self.df[self._columns['High']]
        df_tmp['Low'] = self.df[self._columns['Low']]

        # Calculate Awesome Oscillator
        calculate_ao(df_tmp, column_name)
        df_tmp = df_tmp[[column_name]]
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def accelerator_oscillator(self, column_name='ac'):
        """
        Accelerator Oscillator (AC)
        -----------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/accelerator_decelerator

            >>> Indicators.accelerator_oscillator(column_name='ac')

            :param str column_name: Column name, default: ac
            :return: None
        """
        pass
        # Data frame for storing temporary data
        df_tmp = pd.DataFrame()
        df_tmp['High'] = self.df[self._columns['High']]
        df_tmp['Low'] = self.df[self._columns['Low']]

        # Calculate Awesome Oscillator
        calculate_ao(df_tmp, 'ao')

        # Calculate SMA for Awesome Oscillator
        calculate_sma(df_tmp, 5, 'sma_ao', 'ao')

        # Calculate Accelerator Oscillator
        df_tmp[column_name] = df_tmp['ao'] - df_tmp['sma_ao']
        df_tmp = df_tmp[[column_name]]
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def accumulation_distribution(self, column_name='a/d'):
        """
        Accumulation/Distribution (A/D)
        ---------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/accumulation_distribution

            >>> Indicators.accumulation_distribution(column_name='a/d')

            :param str column_name: Column name, default: a/d
            :return: None

        """
        # Temporary df
        df_tmp = pd.DataFrame()
        df_tmp['close'] = self.df[self._columns['Close']]
        df_tmp['high'] = self.df[self._columns['High']]
        df_tmp['low'] = self.df[self._columns['Low']]
        df_tmp['volume'] = self.df[self._columns['Volume']]

        df_tmp['calc'] = (
                                 (df_tmp['close'] - df_tmp['low']) - (df_tmp['high'] - df_tmp['close'])
                         ) * df_tmp['volume'] / (df_tmp['high'] - df_tmp['low'])

        df_tmp[column_name] = df_tmp['calc'].explode().sum()
        df_tmp = df_tmp[[column_name]]
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def alligator(self,
                  period_jaws=13,
                  period_teeth=8,
                  period_lips=5,
                  shift_jaws=8,
                  shift_teeth=5,
                  shift_lips=3,
                  column_name_jaws='alligator_jaws',
                  column_name_teeth='alligator_teeth',
                  column_name_lips='alligator_lips'):
        """
        Alligator
        ------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/alligator

            >>> Indicators.alligator(period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_jaws='alligator_jaw', column_name_teeth='alligator_teeth', column_name_lips='alligator_lips')

            :param int period_jaws: Period for Alligator' Jaws, default: 13
            :param int period_teeth: Period for Alligator' Teeth, default: 8
            :param int period_lips: Period for Alligator' Lips, default: 5
            :param int shift_jaws: Period for Alligator' Jaws, default: 8
            :param int shift_teeth: Period for Alligator' Teeth, default: 5
            :param int shift_lips: Period for Alligator' Lips, default: 3
            :param str column_name_jaws: Column Name for Alligator' Jaws, default: alligator_jaws
            :param str column_name_teeth: Column Name for Alligator' Teeth, default: alligator_teeth
            :param str column_name_lips: Column Name for Alligator' Lips, default: alligator_lips
            :return: None
        """
        df_median = self.df[[self._columns['High'], self._columns['Low']]]
        median_col = 'median_col'
        df_median = df_median.assign(
            median_col=lambda x: (x[self._columns['High']] + x[self._columns['Low']]) / 2
        )
        df_j = calculate_smma(df_median, period_jaws, column_name_jaws, median_col)
        df_t = calculate_smma(df_median, period_teeth, column_name_teeth, median_col)
        df_l = calculate_smma(df_median, period_lips, column_name_lips, median_col)

        # Shift SMMAs
        df_j[column_name_jaws] = df_j[column_name_jaws].shift(shift_jaws)
        df_t[column_name_teeth] = df_t[column_name_teeth].shift(shift_teeth)
        df_l[column_name_lips] = df_l[column_name_lips].shift(shift_lips)

        self.df = self.df.merge(df_j, left_index=True, right_index=True)
        self.df = self.df.merge(df_t, left_index=True, right_index=True)
        self.df = self.df.merge(df_l, left_index=True, right_index=True)

    def atr(self, period=14, column_name='atr'):
        """
        Average True Range (ATR)
        ------------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/average_true_range

            >>> Indicators.atr(period=14, column_name='atr')

            :param int period: Period, default: 14
            :param str column_name: Column name, default: atr
            :return: None
        """
        df_tmp = self.df[[self._columns['High'], self._columns['Low'], self._columns['Close']]]
        df_tmp = df_tmp.assign(max_min=df_tmp[self._columns['High']] - df_tmp[self._columns['Low']])
        df_tmp['prev_close-high'] = df_tmp[self._columns['Close']].shift(1) - df_tmp[self._columns['High']]
        df_tmp['prev_close-min'] = df_tmp[self._columns['Close']].shift(1) - df_tmp[self._columns['Low']]
        df_tmp['max_val'] = df_tmp.apply(lambda x: max([x['max_min'], x['prev_close-high'], x['prev_close-min']]),
                                         axis=1)
        calculate_sma(df_tmp, period, column_name, 'max_val')
        df_tmp = df_tmp[[column_name]]
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def bears_power(self, period=13, column_name='bears_power'):
        """
        Bears Power
        ------------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/bears_power

            >>> Indicators.bears_power(period=13, column_name='bears_power')

            :param int period: Period, default: 13
            :param str column_name: Column name, default: bears_power
            :return: None
        """
        df_tmp = self.df[[self._columns['Close'], self._columns['Low']]]
        df_tmp = df_tmp.assign(ema=df_tmp[self._columns['Close']].ewm(span=period, adjust=False).mean())
        df_tmp[column_name] = df_tmp['ema'] - df_tmp[self._columns['Low']]
        df_tmp = df_tmp[[column_name]]
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def bollinger_bands(self, period=20, deviation=2, column_name_top='bollinger_top',
                        column_name_mid='bollinger_mid', column_name_bottom='bollinger_bottom'):
        """
        Bollinger Bands
        ---------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/bollinger_bands

            >>> Indicators.bollinger_bands(self, period=20, deviation=2, column_name_top='bollinger_up', column_name_mid='bollinger_mid', column_name_bottom='bollinger_bottom')

            :param int period: Period, default 20
            :param int deviation: Number of Standard Deviations, default 2
            :param str column_name_top: default bollinger_up
            :param str column_name_mid: default bollinger_mid
            :param str column_name_bottom: default bollinger_down
            :return: None
        """
        df_tmp = self.df[[self._columns['Close']]]
        df_tmp = df_tmp.assign(mid=df_tmp[self._columns['Close']].rolling(window=period).mean())
        df_tmp = df_tmp.assign(stdev=df_tmp[self._columns['Close']].rolling(window=period).std(ddof=0))
        df_tmp = df_tmp.assign(tl=df_tmp.mid + deviation * df_tmp.stdev)
        df_tmp = df_tmp.assign(bl=df_tmp.mid - deviation * df_tmp.stdev)

        df_tmp = df_tmp[['mid', 'tl', 'bl']]
        df_tmp = df_tmp.rename(columns={'mid': column_name_mid, 'tl': column_name_top, 'bl': column_name_bottom})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def bulls_power(self, period=13, column_name='bulls_power'):
        """
        Bulls Power
        ------------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/bulls_power

            >>> Indicators.bulls_power(period=13, column_name='bulls_power')

            :param int period: Period, default: 13
            :param str column_name: Column name, default: bulls_power
            :return: None
        """
        df_tmp = self.df[[self._columns['Close'], self._columns['High']]]
        df_tmp = df_tmp.assign(ema=df_tmp[self._columns['Close']].ewm(span=period, adjust=False).mean())
        df_tmp[column_name] = df_tmp[self._columns['High']] - df_tmp['ema']
        df_tmp = df_tmp[[column_name]]
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def cci(self, period=14, column_name='cci'):
        """
        Commodity Channel Index (CCI)
        -----------------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/commodity_channel_index

            >>> Indicators.cci(period=14, column_name='cci')

            :param int period: Period, default: 14
            :param str column_name: Column name, default: cci
            :return: None
        """
        pd.set_option('display.max_columns', 500)
        df_tmp = self.df[[self._columns['High'], self._columns['Low'], self._columns['Close']]]
        df_tmp = df_tmp.assign(tp=(df_tmp[self._columns['High']]
                                   + df_tmp[self._columns['Low']]
                                   + df_tmp[self._columns['Close']]) / 3)

        df_tmp = df_tmp.assign(tp_sma=df_tmp.tp.rolling(window=period).mean())
        df_tmp = df_tmp.assign(tp_mad=df_tmp.tp.rolling(window=period).apply(mad, raw=False))
        df_tmp = df_tmp.assign(tp_min_sma=df_tmp.tp - df_tmp.tp_sma)
        df_tmp = df_tmp.assign(cci=(1 / 0.015) * (df_tmp.tp_min_sma / df_tmp.tp_mad))
        df_tmp = df_tmp[['cci']]
        df_tmp = df_tmp.rename(columns={'cci': column_name})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def de_marker(self, period=14, column_name='dem'):
        """
        DeMarker (DeM)
        --------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/demarker

            >>> Indicators.de_marker(period=14, column_name='dem')

            :param int period: Period, default: 14
            :param str column_name: Column name, default: dem
            :return: None
        """
        df_tmp = self.df[[self._columns['High'], self._columns['Low']]]

        df_tmp = df_tmp.assign(
            hdif=(df_tmp[self._columns['High']] > df_tmp[self._columns['High']].shift(1)).astype(int))
        df_tmp = df_tmp.assign(hsub=df_tmp[self._columns['High']] - df_tmp[self._columns['High']].shift(1))
        df_tmp = df_tmp.assign(demax=np.where(df_tmp.hdif == 0, 0, df_tmp.hsub))

        df_tmp = df_tmp.assign(ldif=(df_tmp[self._columns['Low']] < df_tmp[self._columns['Low']].shift(1)).astype(int))
        df_tmp = df_tmp.assign(lsub=df_tmp[self._columns['Low']].shift(1) - df_tmp[self._columns['Low']])
        df_tmp = df_tmp.assign(demin=np.where(df_tmp.ldif == 0, 0, df_tmp.lsub))

        df_tmp['sma_demax'] = df_tmp['demax'].rolling(window=period).mean()
        df_tmp['sma_demin'] = df_tmp['demin'].rolling(window=period).mean()

        df_tmp = df_tmp.assign(dem=df_tmp.sma_demax / (df_tmp.sma_demax + df_tmp.sma_demin))

        df_tmp = df_tmp[['dem']]
        df_tmp = df_tmp.rename(columns={'dem': column_name})

        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def force_index(self, period=13, method='sma', apply_to='Close', column_name='frc'):
        """
        Force Index (FRC)
        ------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/force_index

            >>> Indicators.force_index(period=13, method='sma', apply_to='Close', column_name='frc')

            :param int period: Period, default: 13
            :param str method: Moving average method. Can be 'sma', 'smma' or 'ema'. Default: sma
            :param str apply_to: Apply indicator to column, default: Close
            :param str column_name: Column name, default: frc
            :return: None
        """
        df_tmp = self.df[[apply_to, self._columns['Volume']]]
        if method == 'sma':
            df_tmp = df_tmp.assign(ma=df_tmp[apply_to].rolling(window=period).mean())
        elif method == 'smma':
            df_tmp_smma = calculate_smma(df_tmp, period, 'ma', apply_to)
            df_tmp = df_tmp.merge(df_tmp_smma, left_index=True, right_index=True)
        elif method == 'ema':
            df_tmp = df_tmp.assign(ma=df_tmp[apply_to].ewm(span=period, adjust=False).mean())
        else:
            raise ValueError('The "method" can be only "sma", "ema" or "smma"')
        df_tmp = df_tmp.assign(frc=(df_tmp.ma - df_tmp.ma.shift(1)) * df_tmp[self._columns['Volume']])
        df_tmp = df_tmp[['frc']]
        df_tmp = df_tmp.rename(columns={'frc': column_name})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def fractals(self, column_name_high='fractals_high', column_name_low='fractals_low'):
        """
        Fractals
        ---------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/fractals

            >>> Indicators.fractals(column_name_high='fractals_high', column_name_low='fractals_low')

            If fractals are high than 1, if fractals are low than -1, else 0

            :param str column_name_high: Column name for High values, default: fractals_high
            :param str column_name_low: Column name for Low values, default: fractals_low
            :return: None
        """
        df_tmp = self.df[[self._columns['High'], self._columns['Low']]]
        df_tmp = df_tmp.assign(fh=np.where(
            (df_tmp[self._columns['High']] > df_tmp[self._columns['High']].shift(1)) &
            (df_tmp[self._columns['High']] > df_tmp[self._columns['High']].shift(2)) &
            (df_tmp[self._columns['High']] > df_tmp[self._columns['High']].shift(-1)) &
            (df_tmp[self._columns['High']] > df_tmp[self._columns['High']].shift(-2)),
            True, False
        ))
        df_tmp = df_tmp.assign(fl=np.where(
            (df_tmp[self._columns['Low']] < df_tmp[self._columns['Low']].shift(1)) &
            (df_tmp[self._columns['Low']] < df_tmp[self._columns['Low']].shift(2)) &
            (df_tmp[self._columns['Low']] < df_tmp[self._columns['Low']].shift(-1)) &
            (df_tmp[self._columns['Low']] < df_tmp[self._columns['Low']].shift(-2)),
            True, False
        ))
        df_tmp = df_tmp[['fh', 'fl']]
        df_tmp = df_tmp.rename(columns={'fh': column_name_high, 'fl': column_name_low})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)
