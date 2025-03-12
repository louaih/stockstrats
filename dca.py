import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
days = 252 * 10  # 10 years of trading days
initial_cash = 100000  # Total cash available for investing
base_investment = 120  # Daily DCA amount
dip_multiplier = 2  # Extra investment multiplier for dips
dip_threshold = -0.05  # 2% daily drop considered a dip

# Simulate market returns (upward drift + daily noise)
np.random.seed(42)
market_returns = np.random.normal(loc=0.0004, scale=0.01, size=days)  # Avg ~10% annual return
market_prices = np.cumprod(1 + market_returns) * 100  # Base price of 100

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
plt.xlabel("Days")
plt.ylabel("Portfolio Value ($)")
plt.title("Investment Strategy Comparison")
plt.legend()
plt.show()

