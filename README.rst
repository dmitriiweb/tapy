tapy
====

Technical Indicators for the Pandas' Dataframes

Documentation: https://pandastechindicators.readthedocs.io/en/latest/

Installation
------------

::

    pip install -U tapy

Example
-------

::


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


Available Indicators
--------------------

1. Accelerator Oscillator (AC)
2. Accumulation/Distribution (A/D)
3. Alligator
4. Average True Range (ATR)
5. Awesome Oscillator (AO)
6. Bears Power
7. Exponential Moving Average (EMA)
8. Simple Moving Average (SMA)
9. Smoothed Moving Average (SMMA)
