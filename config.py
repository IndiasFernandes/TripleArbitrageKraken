# Configuration file for the arbitrage bot

# --- Trading Pairs Configuration ---
# Currently, only USDT is supported as the base currency
base_currency = 'USDT'

# Second currency is BTC, represented as XXBT on Kraken
second_currency = 'BTC'

# List of third currencies for trading pairs
third_currency_list = ['ETH', 'ADA', 'SOL', 'ALGO', 'ATOM', 'BCH']

# The primary trading pair to be used for arbitrage
first_pair = second_currency + base_currency  # Format: XXBTUSDT

# --- Trading Parameters ---
# Percentage of full amount to trade (e.g., 0.999 means 99.9% of the full amount)
percentage_of_full_amount = 0.98  # Range: 0 (0%) to 1 (100%)

# Desired profit threshold to trigger a trade
threshold_profit = 0.02  # Example: 0.02 for 2%

# Interval (in seconds) to check orders on the exchange
check_order_interval = 0.01  # Example: 0.01 for 10 milliseconds
