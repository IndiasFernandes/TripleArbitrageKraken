# Crypto Arbitrage Bot

This project was developed by Indias Fernandes, a developer specialized in crafting market instruments for both backend and frontend applications, forex, stocks and crypto. Indias is open for collaborations and freelance projects via [Fiverr](https://www.fiverr.com/indias) and [Upwork](https://www.upwork.com/freelancers/danielf26).

This bot identifies arbitrage opportunities across various cryptocurrency pairs on Kraken and executes trades to capitalize on price discrepancies. The bot is written in Python and interacts with the Kraken API to monitor prices and execute trades.

## Features

- Identifies and acts on arbitrage opportunities in real-time.
- Supports multiple cryptocurrency pairs.
- Configurable profit threshold for trade execution.
- Colorful logging for easy monitoring.

## Prerequisites

Before running the bot, ensure you have the following prerequisites installed:

- Python 3.8 or above
- PyCharm (optional, for development)
- A Kraken account with necessary API credentials.

## Installation

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/your-username/crypto-arbitrage-bot.git
    ```
    
2. Navigate to the project directory:
    ```bash
    cd crypto-arbitrage-bot
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Setup your Kraken API credentials:
    - Create a `kraken.key` file in the project root directory.
    - Copy your API key and API secret from Kraken to `kraken.key`, formatted as follows:
        ```
        API_KEY
        API_SECRET
        ```

## Usage

1. Update the `config.py` file with your desired trading pairs, threshold profit, and other settings.
   
2. Run the `arbitrage_bot.py` script to start the bot:
    ```bash
    python arbitrage_bot.py
    ```

3. Monitor the console for logging information about potential arbitrage opportunities and executed trades.
