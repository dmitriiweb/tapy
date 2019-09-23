def calculate_sma(df, period, column_name, apply_to):
    df[column_name] = df[apply_to].rolling(window=period).mean()
