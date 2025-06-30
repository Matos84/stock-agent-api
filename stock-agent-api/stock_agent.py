import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

def get_stock_data(symbol, period="6mo"):
    print(f"מוריד נתונים עבור {symbol}...")
    data = yf.download(symbol, period=period)
    if data.empty:
        print("לא נמצאו נתונים.")
        return None
    return data

def add_moving_averages(df, short_window=20, long_window=50):
    df["MA_short"] = df["Close"].rolling(window=short_window).mean()
    df["MA_long"] = df["Close"].rolling(window=long_window).mean()
    return df

def show_table(df):
    print(df.tail(10))

def plot_stock(df, symbol):
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df["Close"], label="מחיר סגירה")
    plt.plot(df.index, df["MA_short"], label="ממוצע נע קצר (20)")
    plt.plot(df.index, df["MA_long"], label="ממוצע נע ארוך (50)")
    plt.title(f"{symbol} - מחיר וממוצעים נעים")
    plt.xlabel("תאריך")
    plt.ylabel("מחיר")
    plt.legend()
    plt.show()

def agent_chat():
    print("Welcome to the Stock Analysis Assistant!")
    symbol = input("Which stock do you want to analyze? (e.g. AAPL): ").upper()
    period = input("For which period? (default 6mo): ") or "6mo"

    data = get_stock_data(symbol, period)
    if data is None:
        return

    data = add_moving_averages(data)
    show_table(data)
    plot_stock(data, symbol)

if __name__ == "__main__":
    agent_chat()
