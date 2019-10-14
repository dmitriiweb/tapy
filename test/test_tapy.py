import unittest

import pandas as pd

from tapy import Indicators


class TestIndicators(unittest.TestCase):
    """
    For test purposes use EURUSD 60 min 2019.02.15 14:00 -- 2019.09.20 20:00
    """

    def setUp(self):
        self.df = pd.read_csv('EURUSD60.csv')
        self.indicators = Indicators(self.df)

    def test_sma(self):
        col = 'sma'
        self.indicators.sma(period=5, column_name=col)
        df = self.indicators.df
        val = get_val(df, col, -1, 5)
        self.assertEqual(1.10151, val)

    def test_ema(self):
        col = 'ema'
        self.indicators.ema(period=5, column_name=col)
        df = self.indicators.df
        val = get_val(df, col, -1, 5)
        self.assertEqual(1.10164, val)

    def test_awesome_oscillator(self):
        col = 'ao'
        self.indicators.awesome_oscillator(column_name=col)
        df = self.indicators.df
        val = get_val(df, col, -1, 6)
        self.assertEqual(-0.002834, val)

    def test_accelerator_oscillator(self):
        col = 'ac'
        self.indicators.accelerator_oscillator(column_name=col)
        df = self.indicators.df
        val = get_val(df, col, -1, 7)
        self.assertEqual(0.0003882, val)

    def test_accumulation_distribution(self):
        col = 'a/d'
        self.indicators.accumulation_distribution(column_name=col)
        df = self.indicators.df
        val = get_val(df, col, -1, 0)
        self.assertEqual(-51439.0, val)

    def test_smma(self):
        col = 'smma'
        self.indicators.smma(period=5, column_name=col)
        df = self.indicators.df
        val = get_val(df, col, -1, 5)
        self.assertEqual(1.10192, val)

    def test_alligator(self):
        col_jaws = 'jaws'
        col_teeth = 'teeth'
        col_lips = 'lips'
        self.indicators.alligator(column_name_jaws=col_jaws,
                                  column_name_teeth=col_teeth, column_name_lips=col_lips)
        df = self.indicators.df
        val_jaws = get_val(df, col_jaws, -1, 5)
        val_teeth = get_val(df, col_teeth, -1, 5)
        val_lips = get_val(df, col_lips, -1, 5)
        self.assertEqual(1.10478, val_jaws)
        self.assertEqual(1.10352, val_teeth)
        self.assertEqual(1.10214, val_lips)

    def test_atr(self):
        col = 'atr'
        self.indicators.atr(column_name=col)
        df = self.indicators.df
        val_atr = get_val(df, col, -1, 4)
        self.assertEqual(0.0013, val_atr)

    def test_bears_power(self):
        col = 'bears'
        self.indicators.bears_power(column_name=col)
        df = self.indicators.df
        val_bears = get_val(df, col, -1, 5)
        self.assertEqual(0.00083, val_bears)

    def test_bollinger_bands(self):
        col_up = 'bollinger_up'
        col_mid = 'bollinger_mid'
        col_down = 'bollinger_down'
        self.indicators.bollinger_bands(column_name_top=col_up, column_name_mid=col_mid, column_name_bottom=col_down)
        df = self.indicators.df
        val_up = get_val(df, col_up, -1, 5)
        val_mid = get_val(df, col_mid, -1, 5)
        val_down = get_val(df, col_down, -1, 5)
        self.assertEqual(1.10733, val_up)
        self.assertEqual(1.10346, val_mid)
        self.assertEqual(1.09959, val_down)

    def test_bulls_power(self):
        col = 'bulls'
        self.indicators.bulls_power(column_name=col)
        df = self.indicators.df
        val_bulls = get_val(df, col, -1, 5)
        self.assertEqual(-0.00015, val_bulls)

    def test_cci(self):
        col = 'cci'
        self.indicators.cci(column_name=col)
        df = self.indicators.df
        val_cci = get_val(df, col, -1, 4)
        self.assertEqual(-38.4801, val_cci)

    def test_de_marker(self, period=14, column_name='dem'):
        col = 'dem'
        self.indicators.de_marker(column_name=col)
        df = self.indicators.df
        val_dem = get_val(df, col, -1, 4)
        self.assertEqual(0.1967, val_dem)

    def test_force_index_error(self):
        col = 'frc'
        with self.assertRaises(Exception) as context:
            self.indicators.force_index(column_name=col, method='blah')
        self.assertTrue('The "method" can be only "sma", "ema" or "smma"')

    def test_force_index(self):
        col_sma = 'frc_sma'
        col_ema = 'ema'
        col_smma = 'smma'
        self.indicators.force_index(column_name=col_sma)
        self.indicators.force_index(column_name=col_ema, method='ema')
        self.indicators.force_index(column_name=col_smma, method='smma')
        self.indicators.force_index()
        df = self.indicators.df
        val_frc_sma = get_val(df, col_sma, -1, 4)
        val_frc_ema = get_val(df, col_ema, -1, 4)
        val_frc_smma = get_val(df, col_smma, -1, 4)
        self.assertEqual(-0.3154, val_frc_sma)
        self.assertEqual(-0.1294, val_frc_ema)
        self.assertEqual(-0.1495, val_frc_smma)


def get_val(df, column, val_index, round_to):
    val = round(df[column].tolist()[val_index], round_to)
    return val
