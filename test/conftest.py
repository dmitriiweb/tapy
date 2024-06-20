import pytest
import pandas as pd


from tapy import Indicators


@pytest.fixture()
def indicators() -> Indicators:
    df = pd.read_csv("EURUSD60.csv")
    indicators = Indicators(df)
    return indicators
