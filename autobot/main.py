import ccxt
import pandas as pd
import time
from discord_webhook import DiscordWebhook
from config import *
from signal_logic import detect_signal

exchange = ccxt.binance()

def fetch_candles(pair, tf):
    ohlcv = exchange.fetch_ohlcv(pair, tf, limit=100)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df

def send_signal(signal, pair, tf):
    message = f"""🔥 AUTO SIGNAL: {pair} – {signal['type']}

🕒 Timeframe: {tf}
📍 Entry: {signal['entry']}
🛑 Stop Loss: {signal['sl']}
🎯 Take Profit: {signal['tp']}
📊 Reason: {signal['reason']}
✅ Confidence: AUTO DETECTED

📉 Skenario Jika SL:
- Tunggu struktur reversal valid di zona: {signal['reentry_zone']}  
- Re-entry bisa dipertimbangkan jika ada validasi candle/pattern

📈 Skenario Jika TP:
- Lanjutkan pantau HL berikutnya
- Atur trailing stop jika perlu
"""
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK, content=message)
    webhook.execute()

while True:
    try:
        for pair in PAIRS:
            for tf in TIMEFRAMES:
                df = fetch_candles(pair, tf)
                signal = detect_signal(df)
                if signal:
                    send_signal(signal, pair, tf)
                time.sleep(2)  # Hindari spam API Binance
        time.sleep(60)  # Delay antar scan
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(60)
