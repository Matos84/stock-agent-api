from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
CORS(app)


# לוודא שיש תיקיה לשמירת תמונות
if not os.path.exists("static"):
    os.makedirs("static")

def get_stock_data(symbol, period="6mo"):
    # נוריד עם auto_adjust כדי לקבל Close רגיל בלי Adj Close
    data = yf.download(symbol, period=period, auto_adjust=True)
    if data.empty:
        return data

    # לפשט עמודות אם זה MultiIndex
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = ['_'.join(col).strip() for col in data.columns.values]
    
    data = data.reset_index()
    return data

def find_close_column(df):
    for col in df.columns:
        if 'Close' in col:
            return col
    return None

def add_moving_averages(df, short_window=20, long_window=50):
    close_col = find_close_column(df)
    if close_col is None:
        raise Exception("No column containing 'Close' found in DataFrame!")
    
    df["MA_short"] = df[close_col].rolling(window=short_window).mean()
    df["MA_long"] = df[close_col].rolling(window=long_window).mean()
    return df

def plot_stock_and_save(df, symbol):
    close_col = find_close_column(df)
    if close_col is None:
        close_col = 'Close'
    
    filename = f"static/{symbol}_chart.png"
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df[close_col], label=f"{close_col} Price")
    plt.plot(df.index, df["MA_short"], label="Short MA (20)")
    plt.plot(df.index, df["MA_long"], label="Long MA (50)")
    plt.title(f"{symbol} - Price and Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.savefig(filename)
    plt.close()
    return filename

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    symbol = data.get("symbol")
    period = data.get("period", "6mo")

    if not symbol:
        return jsonify({"error": "סימבול מניה נדרש."})

    df = get_stock_data(symbol, period)
    if df is None or df.empty:
        return jsonify({"error": "לא נמצאו נתונים למניה/תקופה שביקשת."})

    # לפשט עמודות שוב למקרה שהגיע משהו מורכב
    df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

    try:
        df = add_moving_averages(df)
    except Exception as e:
        return jsonify({"error": f"שגיאה בחישוב ממוצעים נעים: {str(e)}"})

    df = df.reset_index(drop=True)
    last_rows = df.tail(10).to_dict(orient="records")
    chart_path = plot_stock_and_save(df, symbol)

    response = {
        "symbol": symbol,
        "period": period,
        "table": last_rows,
        "chart_url": f"/{chart_path}"
    }

    return jsonify(response)

@app.route("/")
def home():
    return "Stock Agent API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
