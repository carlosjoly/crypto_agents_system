import pandas as pd
import numpy as np

def calculate_indicators(prices, volumes, rsi_period=14, atr_period=14):
    if not prices or len(prices) < rsi_period + 2:
        return None

    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['volume'] = [v[1] for v in volumes[:len(df)]]
    
    # Variação e RSI
    delta = df['price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # Volume Relativo
    df['vol_ma'] = df['volume'].rolling(window=20).mean()
    df['volume_relative'] = df['volume'] / df['vol_ma']
    
    # ATR Simplificado
    df['high_low'] = df['price'] * 0.01  # Estimativa de volatilidade base
    df['atr'] = df['high_low'].rolling(window=atr_period).mean()
    
    return df
