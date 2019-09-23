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


def get_val(df, column, val_index, round_to):
    val = round(df[column].tolist()[val_index], round_to)
    return val
