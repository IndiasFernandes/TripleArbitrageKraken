import krakenex
import logging

# Configure API
market = krakenex.API()
client = krakenex.API()
client.load_key('kraken.key')

def get_balances(assets):
    """Fetch balances for a list of assets."""

    if isinstance(assets, list):

        response = client.query_private('Balance')
        if response['error']:
            logging.error(f"Error fetching balances: {response['error']}")
            return None
        return {asset: float(response['result'].get(asset, 0)) for asset in assets}
    else:
        response = client.query_private('Balance')
        if response['error']:
            logging.error(f"Error fetching balances: {response['error']}")
            return None
        return float(response['result'].get(assets, 0))

def get_all_pairs():
    """Fetch all available pairs on Kraken."""
    pairs = market.query_public('AssetPairs')
    return [pair for pair in pairs['result']]

def get_prices(pairs):
    """Fetch the current price for a list of pairs."""
    tickers = client.query_public('Ticker', {'pair': ','.join(pairs)})
    if tickers['error']:
        logging.error(f"Error fetching tickers: {tickers['error']}")
        return None
    return {pair: float(tickers['result'][pair]['c'][0]) for pair in tickers['result']}

def execute_market_trade(pair, trade_type, volume):
    """Execute a market trade on Kraken."""
    response = client.query_private(
        'AddOrder',
        {
            'pair': pair,
            'type': trade_type,
            'ordertype': 'market',
            'volume': str(volume)
        }
    )
    if response['error']:
        logging.error(f"Error placing order: {response['error']}")
        return None
    logging.info(f"Order placed successfully: {response['result']}")
    return response

def get_normalized_pair(pair):
    """Normalize the pairs according to Kraken's naming convention."""
    replacements = {
        'BTC': 'XBT',
        'ETH': 'ETH',
        'ADA': 'ADA',
        'SOL': 'SOL',
        'BCH': 'BCH',
        'ALGO': 'ALGO',
        'ATOM': 'ATOM'
    }
    for original, replacement in replacements.items():
        pair = pair.replace(original, replacement)

    # Exception for XBT
    if pair == 'ETHXBT':
        pair = 'XETHXXBT'


    return pair
