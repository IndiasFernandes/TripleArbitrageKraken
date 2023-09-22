import time
import logging
from colorama import Fore, Back, Style, init
from config import (
    first_pair, threshold_profit, base_currency,
    second_currency, third_currency_list, percentage_of_full_amount
)
from kraken_interface import (
    get_balances, get_prices, execute_market_trade, get_normalized_pair, get_all_pairs
)

# Configure logging
logging.basicConfig(level=logging.INFO)

def arbitrage_opportunity(prices, base_amount, first_pair, second_pair, third_pair):
    """Calculate the potential profit from an arbitrage opportunity."""
    first_pair_price = prices[first_pair]
    second_pair_price = prices[second_pair]
    third_pair_price = prices[third_pair]

    second_amount = base_amount / first_pair_price
    third_amount = second_amount / second_pair_price
    final_base_amount = third_amount * third_pair_price

    potential_profit = final_base_amount - base_amount
    return potential_profit


# Initialize colorama
init()

# Give Colours to Text in Python
class ColorfulFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            if "Applying Arbitrage" in record.msg:
                return Fore.GREEN + super().format(record) + Style.RESET_ALL
            elif "Arbitrage Opportunity" in record.msg:
                return Fore.YELLOW + super().format(record) + Style.RESET_ALL
            elif "No arbitrage opportunity" in record.msg:
                return Fore.RED + super().format(record) + Style.RESET_ALL
            else:
                return Fore.LIGHTWHITE_EX + super().format(record) + Style.RESET_ALL
        return super().format(record)

# Set up logging to use the colorful formatter, and only include the message in the output
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
    format='%(message)s'
)

# Replace the default formatter on the first handler with the ColorfulFormatter
logging.getLogger().handlers[0].setFormatter(ColorfulFormatter('%(message)s'))


if __name__ == '__main__':
    logging.info("Starting Arbitrage Bot")

    # Get Base Currency Balance
    balance_base = float(get_balances(base_currency))
    logging.info(f"Base Balance: {balance_base}")

    # Convert BTC to USDT (exception)
    balance_second_currency = float(get_balances('XXBT'))
    logging.info(f"BTC Balance: {balance_second_currency}")
    if balance_second_currency != 0:
        logging.info(f"Converting {second_currency} to {base_currency}")
        response = execute_market_trade(
            'XBTUSDT',
            'sell',
            balance_second_currency
        )
        logging.info(f"Conversion response: {response}")

    # Start by converting all the coins back to USDT
    for currency in third_currency_list:
        balances = get_balances([currency])
        logging.info(f"{currency} Balance: {balances[currency]}")
        if balances[currency] != 0:
            logging.info(f"Converting {currency} to {base_currency}")
            response = execute_market_trade(
                get_normalized_pair(currency + base_currency),
                'sell',
                balances[currency]
            )
            logging.info(f"Conversion response: {response}")

    while True:

        # Get All Pairs in Kraken
        pairs = get_all_pairs()

        # Filter Pairs according to base currency
        all_pairs = [pair for pair in pairs if pair.endswith(base_currency) or pair.endswith(second_currency) or pair.endswith(get_normalized_pair(second_currency))]
        print(all_pairs)
        # Get Balances
        prices = get_prices(all_pairs)

        for third_currency in third_currency_list:
            second_pair = get_normalized_pair(third_currency + second_currency)
            third_pair = get_normalized_pair(third_currency + base_currency)
            normalized_first_pair = get_normalized_pair(first_pair)

            potential_profit = arbitrage_opportunity(
                prices,
                balance_base,
                normalized_first_pair,
                second_pair,
                third_pair
            )

            logging.info(f"Verifying Arbitrage for {base_currency} -> {second_currency} -> {third_currency}")

            if potential_profit >= threshold_profit:
                logging.info(f"Applying Arbitrage: {potential_profit:.3f} {base_currency}")

                # Determine the volume to trade for the first pair
                volume_to_trade = round(
                    balance_base / prices[normalized_first_pair] * percentage_of_full_amount, 5)
                logging.info(
                    f'Volume to Trade ({percentage_of_full_amount * 100}% of {normalized_first_pair}) : {volume_to_trade}')

                # Execute the first trade
                response = execute_market_trade(normalized_first_pair, 'buy', volume_to_trade)
                if response is None:
                    logging.error("Trade failed. Exiting.")
                    break  # Exit loop on failed trade

                # Wait for the first order to complete
                if second_currency == 'XBT':
                    while get_balances('XXBT') == 0:
                        print(f"Balance of {second_currency}: {get_balances('XXBT')}")
                        logging.info("Waiting for order to complete...")
                        time.sleep(2)
                else:
                    while get_balances([second_currency])[second_currency] == 0:
                        print(f"Balance of {second_currency}: {get_balances([second_currency])[second_currency]}")
                        logging.info("Waiting for order to complete...")
                        time.sleep(2)

                # Determine the volume to trade for the second pair
                volume_to_trade = round(
                    get_balances([second_currency])[second_currency] / prices[second_pair] * percentage_of_full_amount,
                    5)
                logging.info(
                    f'Volume to Trade ({percentage_of_full_amount * 100}% of {second_pair}) : {volume_to_trade}')

                # Execute the second trade
                response = execute_market_trade(second_pair, 'buy', volume_to_trade)
                if response is None:
                    logging.error("Trade failed. Exiting.")
                    break  # Exit loop on failed trade

                # Wait for the second order to complete
                while get_balances([third_currency])[third_currency] == 0:
                    logging.info("Waiting for order to complete...")
                    time.sleep(2)

                # Determine the volume to trade for the third pair
                volume_to_trade = get_balances([third_currency])[third_currency]
                logging.info(f'Volume to Trade (100% of total) : {volume_to_trade}')

                # Execute the third trade
                response = execute_market_trade(third_pair, 'sell', volume_to_trade)
                if response is None:
                    logging.error("Trade failed. Exiting.")
                    break  # Exit loop on failed trade

                # Update the current amount
                final_amount = get_balances([base_currency])[base_currency]
                logging.info(
                    f"Arbitrage Completed. Profit: {final_amount - balance_base:.3f} {base_currency}\n")

            elif threshold_profit > potential_profit > 0:
                logging.info(f"Arbitrage Opportunity: {potential_profit:.5f} {base_currency}")

            else:
                logging.info(f"No arbitrage opportunity: {potential_profit:.3f} {base_currency}")

            time.sleep(2)
