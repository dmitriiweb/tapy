import pytest

from tapy import Indicators


def get_val(df, column, val_index, round_to):
    val = round(df[column].tolist()[val_index], round_to)
    return val


def test_sma(indicators: Indicators):
    col = "sma"
    indicators.sma(period=5, column_name=col)
    df = indicators.df
    val = get_val(df, col, -1, 5)
    assert val == 1.10151


def test_ema(indicators: Indicators):
    col = "ema"
    indicators.ema(period=5, column_name=col)
    df = indicators.df
    val = get_val(df, col, -1, 5)
    assert val == 1.10164


def test_awesome_oscillator(indicators: Indicators):
    col = "ao"
    indicators.awesome_oscillator(column_name=col)
    df = indicators.df
    val = get_val(df, col, -1, 6)
    assert val == -0.002834


def test_accelerator_oscillator(indicators: Indicators):
    col = "ac"
    indicators.accelerator_oscillator(column_name=col)
    df = indicators.df
    val = get_val(df, col, -1, 7)
    assert val == 0.0003882


def test_accumulation_distribution(indicators: Indicators):
    col = "a/d"
    indicators.accumulation_distribution(column_name=col)
    df = indicators.df
    val = get_val(df, col, -1, 0)
    assert val == -51439.0


def test_smma(indicators: Indicators):
    col = "smma"
    indicators.smma(period=5, column_name=col)
    df = indicators.df
    val = get_val(df, col, -1, 5)
    assert val == 1.10192


def test_alligator(indicators: Indicators):
    col_jaws = "jaws"
    col_teeth = "teeth"
    col_lips = "lips"
    indicators.alligator(
        column_name_jaws=col_jaws,
        column_name_teeth=col_teeth,
        column_name_lips=col_lips,
    )
    df = indicators.df
    val_jaws = get_val(df, col_jaws, -1, 5)
    val_teeth = get_val(df, col_teeth, -1, 5)
    val_lips = get_val(df, col_lips, -1, 5)

    assert val_jaws == 1.10478
    assert val_teeth == 1.10352
    assert val_lips == 1.10214


def test_atr(indicators: Indicators):
    col = "atr"
    indicators.atr(column_name=col)
    df = indicators.df
    val_atr = get_val(df, col, -1, 4)
    assert val_atr == 0.0013


def test_bears_power(indicators: Indicators):
    col = "bears"
    indicators.bears_power(column_name=col)
    df = indicators.df
    val_bears = get_val(df, col, -1, 5)
    assert val_bears == 0.00083


def test_bollinger_bands(indicators: Indicators):
    col_up = "bollinger_up"
    col_mid = "bollinger_mid"
    col_down = "bollinger_down"
    indicators.bollinger_bands(
        column_name_top=col_up, column_name_mid=col_mid, column_name_bottom=col_down
    )
    df = indicators.df
    val_up = get_val(df, col_up, -1, 5)
    val_mid = get_val(df, col_mid, -1, 5)
    val_down = get_val(df, col_down, -1, 5)

    assert val_up == 1.10733
    assert val_mid == 1.10346
    assert val_down == 1.09959


def test_bulls_power(indicators: Indicators):
    col = "bulls"
    indicators.bulls_power(column_name=col)
    df = indicators.df
    val_bulls = get_val(df, col, -1, 5)
    assert val_bulls == -0.00015


def test_cci(indicators: Indicators):
    col = "cci"
    indicators.cci(column_name=col)
    df = indicators.df
    val_cci = get_val(df, col, -1, 4)
    assert val_cci == -38.4801


def test_de_marker(indicators: Indicators, period=14, column_name="dem"):
    col = "dem"
    indicators.de_marker(column_name=col)
    df = indicators.df
    val_dem = get_val(df, col, -1, 4)
    assert val_dem == 0.1967


def test_force_index_error(indicators: Indicators):
    col = "frc"
    with pytest.raises(Exception) as exception:
        indicators.force_index(column_name=col, method="blah")

    assert str(exception.value) == 'The "method" can be only "sma", "ema" or "smma"'


def test_force_index(indicators: Indicators):
    col_sma = "frc_sma"
    col_ema = "ema"
    col_smma = "smma"
    indicators.force_index(column_name=col_sma)
    indicators.force_index(column_name=col_ema, method="ema")
    indicators.force_index(column_name=col_smma, method="smma")
    indicators.force_index()
    df = indicators.df
    val_frc_sma = get_val(df, col_sma, -1, 4)
    val_frc_ema = get_val(df, col_ema, -1, 4)
    val_frc_smma = get_val(df, col_smma, -1, 4)

    assert val_frc_sma == -0.3154
    assert val_frc_ema == -0.1294
    assert val_frc_smma == -0.1495


def test_fractals(indicators: Indicators):
    col_high = "fh"
    col_low = "fl"
    indicators.fractals(column_name_high=col_high, column_name_low=col_low)
    df = indicators.df
    fractal_low = df.iloc[-6][col_low]
    fractal_high = df.iloc[-14][col_high]
    print(f"{df.iloc[-5][col_low]=}")

    assert fractal_low is not None
    assert fractal_high is not None
    assert df.iloc[-5][col_low] == False


def test_gator(indicators: Indicators):
    col_val1 = "val1"
    col_val2 = "val2"
    indicators.gator(column_name_val1=col_val1, column_name_val2=col_val2)
    df = indicators.df
    val1 = get_val(df, col_val1, -1, 6)
    val2 = get_val(df, col_val2, -1, 6)
    assert val1 == 0.001263
    assert val2 == -0.001376


def test_ichimoku_kinko_hyo(indicators: Indicators):
    col_chikou = "chikou"
    col_tenkan = "tenkan"
    col_kijun = "kijun"
    col_sb = "sb"
    col_sa = "sa"
    indicators.ichimoku_kinko_hyo(
        column_name_chikou_span=col_chikou,
        column_name_tenkan_sen=col_tenkan,
        column_name_kijun_sen=col_kijun,
        column_name_senkou_span_b=col_sb,
        column_name_senkou_span_a=col_sa,
    )
    df = indicators.df
    val_chikou = get_val(df, col_chikou, -27, 5)
    val_tenkan = get_val(df, col_tenkan, -1, 5)
    val_kijun = get_val(df, col_kijun, -1, 5)
    val_sb = get_val(df, col_sb, -1, 5)
    val_sa = get_val(df, col_sa, -1, 5)
    assert val_chikou == 1.10167
    assert val_tenkan == 1.10147
    assert val_kijun == 1.10316
    assert val_sb == 1.10442
    assert val_sa == 1.10494


def test_bw_mfi(indicators: Indicators):
    col = "bw"
    indicators.bw_mfi(column_name=col)
    df = indicators.df
    val_bw = get_val(df, col, -1, 4)
    assert val_bw == 0.0556


def test_momentum(indicators: Indicators):
    col = "mom"
    indicators.momentum(column_name=col)
    df = indicators.df
    val = get_val(df, col, -1, 4)
    assert val == 99.6094


def test_mfi(indicators: Indicators):
    col = "mfi"
    indicators.mfi(column_name=col)
    df = indicators.df
    val = get_val(df, col, -2, 4)
    assert val == 70.6982


def test_macd(indicators: Indicators):
    col_val = "val"
    col_signal = "signal"
    indicators.macd(column_name_value=col_val, column_name_signal=col_signal)
    df = indicators.df
    value = get_val(df, col_val, -1, 6)
    signal = get_val(df, col_signal, -1, 6)
    assert value == -0.000973
    assert signal == -0.000827


def test_alma(indicators: Indicators):
    col = "alma"
    indicators.alma(column_name=col)
    df = indicators.df
    value = get_val(df, col, -1, 6)
    assert value == 1.101739
