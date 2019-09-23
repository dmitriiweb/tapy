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

    def get_val(self, column, val_index, round_to):
        val = round(self.df[column].tolist()[val_index], round_to)
        del self.df[column]
        return val

    def test_sma(self):
        col = 'sma'
        self.indicators.sma(period=5, column_name=col)
        val = self.get_val(col, -1, 5)
        self.assertEqual(1.10151, val)

    def test_ema(self):
        col = 'ema'
        self.indicators.ema(period=5, column_name=col)
        val = self.get_val(col, -1, 5)
        self.assertEqual(1.10164, val)

    def test_awesome_oscillator(self):
        col = 'ao'
        self.indicators.awesome_oscillator(column_name=col)
        val = self.get_val(col, -1, 6)
        self.assertEqual(-0.002834, val)

    def test_accelerator_oscillator(self):
        col = 'ac'
        self.indicators.accelerator_oscillator(column_name=col)
        val = self.get_val(col, -1, 7)
        self.assertEqual(0.0003882, val)
