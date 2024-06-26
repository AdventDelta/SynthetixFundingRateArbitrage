from web3 import *
from dotenv import load_dotenv
from GlobalUtils.logger import *
from GlobalUtils.globalUtils import GLOBAL_SYNTHETIX_CLIENT
import json

load_dotenv()

class MarketDirectory:
    _markets = {}
    _file_path = 'markets.json'
    _is_initialized = False

    @classmethod
    def initialize(cls):
        try:
            if not cls._is_initialized:
                cls.update_all_market_parameters()
                cls._is_initialized = True
                logger.info('MarketDirectory - Markets Initialized')
                with open(cls._file_path, 'r') as file:
                    cls._markets = json.load(file)
        except FileNotFoundError:
            logger.error("MarketDirectory - No existing market file found. Starting fresh.")
        except json.JSONDecodeError:
            logger.error("MarketDirectory - Error decoding JSON. Starting with an empty dictionary.")

    @classmethod
    def save_market_to_file(cls):
        try:
            with open(cls._file_path, 'w') as file:
                json.dump(cls._markets, file)
        except Exception as e:
            logger.error(f"MarketDirectory - Failed to save markets to file: {e}")

    @classmethod
    def load_markets_from_file(cls):
        try:
            with open('markets.json', 'r') as f:
                cls._markets = json.load(f)
        except FileNotFoundError:
            logger.error("MarketDirectory - Market file not found. Starting with an empty dictionary.")
            cls._markets = {}

    @classmethod
    def update_all_market_parameters(cls):
        client = GLOBAL_SYNTHETIX_CLIENT
        market_data_response = client.perps.markets_by_name
        for symbol, market_data in market_data_response.items():
            cls.update_market_member(market_data)
            cls.save_market_to_file()

    @classmethod
    def update_market_member(cls, market_data):
        symbol = market_data['market_name']

        cls._markets[symbol] = {
            'symbol': symbol,
            'market_id': market_data['market_id'],
            'max_funding_velocity': market_data['max_funding_velocity'],
            'skew_scale': market_data['skew_scale'],
            'maker_fee': market_data['maker_fee'],
            'taker_fee': market_data['taker_fee']
        }

    @classmethod
    def get_market_params(cls, symbol: str) -> dict:
        try:
            market: dict = cls._markets.get(symbol)
            if market:
                return market
            else:
                logger.error(f"MarketDirectory - No data available for market {symbol}.")
                return None
        
        except Exception as e:
            logger.error(f"MarketDirectory - Error while getting market params for {symbol}. market = {market}. Error: {e}")
            return None

    @classmethod
    def get_market_id(cls, symbol: str) -> int:
        try:
            market = cls._markets.get(symbol)
            if market:
                return market['market_id']
            logger.error(f"MarketDirectory - Market symbol '{symbol}' not found in MarketDirectory.")

        except Exception as e:
            logger.error(f'Failed to get market id for symbol: {symbol}, market = {market}. Error: {e}')
            return None


    @classmethod
    def calculate_new_funding_velocity(cls, symbol: str, current_skew: float, trade_size: float) -> float:
        try:
            market_data = cls.get_market_params(symbol)
            c = market_data['max_funding_velocity'] / market_data['skew_scale']
            new_skew = current_skew + trade_size
            new_funding_velocity = c * new_skew
            return new_funding_velocity
        except Exception as e:
            logger.error(f"MarketDirectory - Failed to calculate new funding velocity for {symbol}: {e}")

    @classmethod
    def get_maker_taker_fee(cls, symbol: str, skew: float, is_long: bool) -> float:
        try:
            market = cls.get_market_params(symbol)
            if is_long:
                fee = market['maker_fee'] if skew < 0 else market['taker_fee']
            else:
                fee = market['maker_fee'] if skew > 0 else market['taker_fee']

            return fee
        except Exception as e:
            logger.error(f"MarketDirectory - Failed to determine fee for {symbol} with skew {skew} and is_long {is_long}. Error: {e}")
            return None

