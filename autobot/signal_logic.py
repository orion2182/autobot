import pandas as pd
import ta
from config import TP_MULTIPLIER, SL_MULTIPLIER, VOLUME_SPIKE_MULTIPLIER

def detect_signal(df):
    df['ema20'] = ta.trend.ema_indicator(df['close'], 20)
    df['vol_avg'] = df['volume'].rolling(20).mean()

    latest = df.iloc[-1]

    # Kondisi EMA Bounce + Volume Spike
    if latest['close'] > latest['ema20'] and latest['volume'] > VOLUME_SPIKE_MULTIPLIER * latest['vol_avg']:
        entry = round(latest['close'], 4)
        tp = round(entry * TP_MULTIPLIER, 4)
        sl = round(entry * SL_MULTIPLIER, 4)
        reentry_zone = round(entry * 0.995, 4)

        return {
            'type': 'LONG',
            'entry': entry,
            'sl': sl,
            'tp': tp,
            'reason': 'EMA bounce + breakout volume',
            'reentry_zone': reentry_zone
        }

    return None
