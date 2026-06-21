import yfinance as yf

ticker = yf.Ticker("TCS.NS")

print("History:")
print(ticker.history(period="5d"))

print("\nFast Info:")
try:
    print(ticker.fast_info)
except Exception as e:
    print(e)

print("\nInfo:")
try:
    print(ticker.info)
except Exception as e:
    print(e)