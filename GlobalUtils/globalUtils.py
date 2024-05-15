from web3 import *
import os
from dotenv import load_dotenv
import requests
from decimal import Decimal, InvalidOperation
from enum import Enum
from GlobalUtils.logger import *
from APICaller.Synthetix.SynthetixUtils import get_synthetix_client
import json

load_dotenv()

BLOCKS_PER_DAY_BASE = 43200
BLOCKS_PER_HOUR_BASE = 1800

class EventsDirectory(Enum):
    CLOSE_ALL_POSITIONS = "close_positions"
    OPPORTUNITY_FOUND = "opportunity_found"
    POSITION_OPENED = "position_opened"
    POSITION_CLOSED = "position_closed"
    TRADE_LOGGED = "trade_logged"

def initialise_client() -> Web3:
    try:
        client = Web3(Web3.HTTPProvider(os.getenv('BASE_PROVIDER_RPC')))
    except Exception as e:
        logger.info(f"GlobalUtils - Error initialising Web3 client: {e}")
        return None 
    return client

def get_gas_price() -> float:
    client = initialise_client()
    if client:
        try:
            price_in_wei = client.eth.gas_price
            price_in_gwei = client.from_wei(price_in_wei, 'gwei')
            return price_in_gwei
        except Exception as e:
            logger.info(f"GlobalUtils - Error fetching gas price: {e}")
    return 0.0

def get_asset_price(asset: str) -> float:
    api_key = os.getenv('COINGECKO_API_KEY')
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={asset}&vs_currencies=usd&x_cg_demo_api_key={api_key}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if asset in data and 'usd' in data[asset]:
                return data[asset]['usd']
            else:
                logger.error(f"Data for {asset} is missing or malformed: {data}")
        else:
            logger.error(f"API call for {asset} returned non-200 status code: {response.status_code}, Response: {response.text}")
            return None
    except requests.exceptions.RequestException as req_e:
        logger.error(f"Request error fetching asset price for {asset}: {req_e}, URL: {url}")
    except ValueError as val_e:
        logger.error(f"JSON decoding error when fetching asset price for {asset}: {val_e}")
    except Exception as e:
        logger.error(f"Unexpected error fetching asset price for {asset}: {e}, URL: {url}")
    return None

def calculate_transaction_cost_usd(total_gas: int) -> float:
    try:
        gas_price_gwei = get_gas_price()
        eth_price_usd = get_asset_price('ethereum')
        gas_cost_eth = (gas_price_gwei * total_gas) / Decimal('1e9')
        transaction_cost_usd = float(gas_cost_eth) * eth_price_usd
        return transaction_cost_usd
    except (InvalidOperation, ValueError) as e:
        logger.info(f"GlobalUtils - Error calculating transaction cost: {e}")
    return 0.0

def get_asset_amount_for_given_dollar_amount(asset: str, dollar_amount: float) -> float:
    try:
        asset_price = get_asset_price(asset)
        asset_amount = dollar_amount / asset_price
        return asset_amount
    except ZeroDivisionError:
        logger.info(f"GlobalUtils - Error calculating asset amount for {asset}: Price is zero")
    return 0.0

def get_dollar_amount_for_given_asset_amount(asset: str, asset_amount: float) -> float:
    try:
        asset_price = get_asset_price(asset)
        dollar_amount = asset_amount * asset_price
        return dollar_amount
    except Exception as e:
        logger.info(f"GlobalUtils - Error converting asset amount to dollar amount for {asset}: {e}")
    return 0.0

def normalize_symbol(symbol: str) -> str:
    return symbol.replace('USDT', '').replace('PERP', '')

def get_full_asset_name(symbol: str) -> str:
    asset_mapping = {
        'btc': 'bitcoin',
        'eth': 'ethereum',
        'snx': 'havven',
        'sol': 'solana',
        'wif': 'dogwifcoin',
        'w': 'wormhole',
        'ena': 'ethena',
        'doge': 'dogecoin',
        'pepe': 'pepe',
        'arb': 'arbitrum',
        'bnb': 'binancecoin'
    }
    return asset_mapping.get(symbol.lower(), symbol)

def adjust_trade_size_for_direction(trade_size: float, is_long: bool) -> float:
    return trade_size if is_long else -trade_size

def get_base_block_number_by_timestamp(timestamp: int) -> int:
    apikey = os.getenv('BASESCAN_API_KEY')
    url = "https://api.basescan.org/api"
    params = {
        'module': 'block',
        'action': 'getblocknobytime',
        'timestamp': timestamp,
        'closest': 'before',
        'apikey': apikey
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == '1' and data.get('message') == 'OK':
            return int(data.get('result'))
        else:
            logger.info(f"GlobalUtils - Basescan API Error: {data}")
            return -1
    except requests.RequestException as e:
        print("GlobalUtils - Basescan API HTTP Request failed:", e)
        return -1

def get_base_block_number() -> int:
    try:
        client = initialise_client()
        block_number = client.eth.block_number
        return block_number
    except Exception as e:
        logger.error(f'GlobalUtils - Error while calling current block number for BASE network: {e}')
        return None

def get_binance_funding_event_schedule(current_block_number: int) -> list:
    try:
        coordination_block = 13664526
        interval_in_blocks = 14400

        intervals_since_last_event = (current_block_number - coordination_block) // interval_in_blocks
        next_funding_event = coordination_block + (intervals_since_last_event + 1) * interval_in_blocks
        next_three_funding_events = [next_funding_event + i * interval_in_blocks for i in range(3)]
        return next_three_funding_events

    except Exception as e:
        logger.error(f'GlobalUtils - Error while calling current block number for BASE network: {e}')
        return None
