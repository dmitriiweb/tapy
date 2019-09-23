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
        self.indicators.sma(column_name=col)
        val = round(self.df[col].tolist()[-1], 5)
        del self.df[col]
        expected_values = 1.10151
        self.assertEqual(expected_values, val)


