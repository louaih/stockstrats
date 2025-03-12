import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

# Fetch S&P 500 historical data
sp500 = yf.download('^GSPC', period='7y', interval='1d')
market_prices = sp500.get('Adj Close', sp500['Close']).values  # Use 'Close' if 'Adj Close' is unavailable

days = len(market_prices)  # Adjust days to match available data
initial_cash = 100000  # Total cash available for investing
base_investment = 120  # Daily DCA amount
dip_multiplier = 4  # Extra investment multiplier for dips
dip_threshold = -0.03  # 2% daily drop considered a dip

# Strategy 1: Dollar-Cost Averaging (DCA)
dca_shares = 0
dca_cash = initial_cash
dca_shares_over_time = []

for price in market_prices:
    if dca_cash >= base_investment:
        dca_shares += base_investment / price
        dca_cash -= base_investment
    dca_shares_over_time.append(dca_shares * price)

# Strategy 2: DCA + Buying the Dip
dca_dip_shares = 0
dca_dip_cash = initial_cash
dca_dip_shares_over_time = []

for i in range(1, days):
    price = market_prices[i]
    previous_price = market_prices[i - 1]
    investment = base_investment
    
    if (price - previous_price) / previous_price < dip_threshold:
        investment *= dip_multiplier  # Buy more on dip
    
    if dca_dip_cash >= investment:
        dca_dip_shares += investment / price
        dca_dip_cash -= investment
    
    dca_dip_shares_over_time.append(dca_dip_shares * price)

# Strategy 3: Lump Sum Investing (LSI)
lsi_shares = initial_cash / market_prices[0]
lsi_value_over_time = lsi_shares * market_prices

# Plot Results
plt.figure(figsize=(12, 6))
plt.plot(dca_shares_over_time, label="DCA", linestyle='dashed')
plt.plot(dca_dip_shares_over_time, label="DCA + Buy the Dip", linestyle='dotted')
plt.plot(lsi_value_over_time, label="Lump Sum Investing", linestyle='solid')
start_day = datetime.now() - timedelta(days=len(dca_dip_shares_over_time))
plt.xlabel(start_day.strftime("Days since %d %B, %Y"))
plt.ylabel("Portfolio Value ($)")
plt.title("Investment Strategy Comparison Using S&P 500 Data")
plt.legend()
plt.show()
