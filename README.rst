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
    >>> indicators.sma(period=3, column_name='SMA_3')
    >>> df.tail()
      	  Date   Time     Open     High      Low    Close  Volume     SMA_3
    2019.09.20  16:00  1.10022  1.10105  1.10010  1.10070    2888  1.100667
    2019.09.20  17:00  1.10068  1.10193  1.10054  1.10184    6116  1.100920
    2019.09.20  18:00  1.10186  1.10194  1.10095  1.10144    3757  1.101327
    2019.09.20  19:00  1.10146  1.10215  1.10121  1.10188    3069  1.101720
    2019.09.20  20:00  1.10184  1.10215  1.10147  1.10167    1224  1.101663


Available Indicators
--------------------

1. SMA (Simple Moving Average)

