import yfinance as yf
from yahoo_fin import stock_info as si
import matplotlib.pyplot as plt
import pickle

# Set the dark background style for plots
plt.style.use("dark_background")

# Stock symbols and respective amounts
stocks = ['AAPL', 'META', 'TSLA', 'ABBV', 'NVDA', 'CCL', 'BABA', 'NSRGY']
amounts = [20, 15, 20, 10, 50, 60, 30, 30]


# Fetch the live price and calculate the total value of each stock
values = [si.get_live_price(stocks[i]) * amounts[i] for i in range(len(stocks))]

# Fetch industry and country data
sectors = [yf.Ticker(x).info.get('industry', 'Unknown') for x in stocks]
countries = [yf.Ticker(x).info.get('country', 'Unknown') for x in stocks]
market_caps = [yf.Ticker(x).info.get('marketCap', 0) for x in stocks]

# Cash available and ETFs
cash = 40000
etfs = ['IVV', 'XWD.TO']
etf_amounts = [30, 20]
etf_values = [si.get_live_price(etfs[i]) * etf_amounts[i] for i in range(len(etfs))]

# Cryptocurrencies and their values
cryptos = ['ETH-USD', 'BTC-USD']
crypto_amounts = [0.89, 0.34]
crypto_values = [si.get_live_price(cryptos[i]) * crypto_amounts[i] for i in range(len(cryptos))]

# General distribution
general_dist = {
    'Stocks': sum(values),
    'ETFs': sum(etf_values),
    'Cryptos': sum(crypto_values),
    'Cash': cash
}

# Sector distribution
sector_dist = {}
for i in range(len(sectors)):
    if sectors[i] not in sector_dist:
        sector_dist[sectors[i]] = 0
    sector_dist[sectors[i]] += values[i]

# Country distribution
country_dist = {}
for i in range(len(countries)):
    if countries[i] not in country_dist:
        country_dist[countries[i]] = 0
    country_dist[countries[i]] += values[i]

# Market cap distribution
market_cap_dist = {'small': 0.0, 'mid': 0.0, 'large': 0.0, 'huge': 0.0}
for i in range(len(market_caps)):
    if market_caps[i] < 1e9:
        market_cap_dist['small'] += values[i]
    elif market_caps[i] < 5e9:
        market_cap_dist['mid'] += values[i]
    elif market_caps[i] < 2e11:
        market_cap_dist['large'] += values[i]
    else:
        market_cap_dist['huge'] += values[i]

# Save data to pickle files
with open('general.pickle', 'wb') as f:
    pickle.dump(general_dist, f)

with open('industry.pickle', 'wb') as f:
    pickle.dump(sector_dist, f)

with open('country.pickle', 'wb') as f:
    pickle.dump(country_dist, f)

with open('market_cap.pickle', 'wb') as f:
    pickle.dump(market_cap_dist, f)

# Create pie charts for distribution analysis
fig, axs = plt.subplots(2, 2)
fig.suptitle('Portfolio Analysis', fontsize=10)

# List of colors from TABLEAU_COLORS
color_scheme = list(plt.cm.Paired.colors)

# General Distribution pie chart
axs[0, 0].pie(general_dist.values(), labels=general_dist.keys(), autopct="%1.1f%%", pctdistance=0.8, colors=color_scheme)
axs[0, 0].set_title('General Distribution')

# Sector by Industry pie chart
axs[0, 1].pie(sector_dist.values(), labels=sector_dist.keys(), autopct="%1.1f%%", pctdistance=0.8, colors=color_scheme)
axs[0, 1].set_title('Sector by Industry')

# Sector by Country pie chart
axs[1, 0].pie(country_dist.values(), labels=country_dist.keys(), autopct="%1.1f%%", pctdistance=0.8, colors=color_scheme)
axs[1, 0].set_title('Sector by Country')

# Market Cap Distribution pie chart
axs[1, 1].pie(market_cap_dist.values(), labels=market_cap_dist.keys(), autopct="%1.1f%%", pctdistance=0.8, colors=color_scheme)
axs[1, 1].set_title('Market Cap Distribution')

# Show the plot
plt.tight_layout()
plt.show()
