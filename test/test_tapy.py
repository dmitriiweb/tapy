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
        val = round(self.df[col].tolist()[-1], 5)
        del self.df[col]
        self.assertEqual(1.10151, val)

    def test_ema(self):
        col = 'ema'
        self.indicators.ema(period=5, column_name=col)
        val = round(self.df[col].tolist()[-1], 5)
        del self.df[col]
        self.assertEqual(1.10164, val)


