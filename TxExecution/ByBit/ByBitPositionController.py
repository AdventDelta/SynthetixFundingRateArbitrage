import sys
sys.path.append('/Users/jfeasby/SynthetixFundingRateArbitrage')

from pybit.unified_trading import HTTP
from APICaller.ByBit.ByBitUtils import *
from pubsub import pub
import os
import json
from dotenv import load_dotenv
import requests
from GlobalUtils.globalUtils import *
from GlobalUtils.logger import logger
from APICaller.master.MasterUtils import TARGET_TOKENS
from TxExecution.ByBit.utils import *

load_dotenv()

class ByBitPositionController:
    
    def __init__(self):
        self.client = get_ByBit_client()
        self.api_key = os.getenv('BYBIT_API_KEY')
        self.api_secret = os.getenv('BYBIT_API_SECRET')
        self.leverage = os.getenv('TRADE_LEVERAGE')
        self.set_leverage_for_all_assets(TARGET_TOKENS)

    #######################
    ### WRITE FUNCTIONS ###
    #######################

    def execute_trade(self, opportunity, is_long: bool, trade_size: float):
        try:
            side = get_side(is_long)
            full_asset_name = get_full_asset_name(opportunity['symbol'])
            trade_size_in_asset = get_asset_amount_for_given_dollar_amount(full_asset_name, trade_size)
            self.client.place_order(
                category="linear",
                symbol=opportunity['symbol'] + 'USDT',
                side=side,
                orderType="Market",
                qty=trade_size_in_asset,
            )
            logger.info(f"ByBit - Trade executed: {opportunity['symbol']} {'Long' if is_long else 'Short'}, Size: {trade_size_in_asset}")
        except Exception as e:
            logger.error(f"ByBit - Failed to execute trade for {opportunity['symbol']}. Error: {e}")


    def close_all_positions(self):
        try:
            self.client.cancel_all_orders(category='linear')
            logger.info("ByBit - All positions closed successfully.")
        except Exception as e:
            logger.error(f"ByBit - Failed to close all positions. Error: {e}")


    def set_leverage_for_all_assets(self, tokens):
        for token in tokens:
            try:
                if token["is_target"]:
                    symbol = token["token"] + "USDT"
                    current_leverage = self.get_leverage_factor_for_token(symbol)
                    if not is_leverage_already_correct(current_leverage, self.leverage):
                        self.client.set_leverage(
                            category="linear",
                            symbol=symbol,
                            buyLeverage=self.leverage,
                            sellLeverage=self.leverage
                        )
                        logger.info(f"ByBit - Leverage set for {symbol}: {self.leverage}x")
            except Exception as e:
                logger.error(f"ByBit - Failed to set leverage for {symbol}. Error: {e}")


    ######################
    ### READ FUNCTIONS ###
    ######################

    def get_leverage_factor_for_token(self, symbol: str) -> float:
        try:
            response = self.client.get_positions(category='linear', symbol=symbol)
            if response['retCode'] == 0 and response['result']['list']:
                leverage_factor = response['result']['list'][0]['leverage']
                return float(leverage_factor)
            else:
                logger.error(f"ByBit - Could not find leverage factor for symbol {symbol}.")
                return 0.0
        except Exception as e:
            logger.error(f"ByBit - Error retrieving leverage factor for {symbol}. Error: {e}")
            return 0.0


    def get_available_collateral(self) -> float:
        try:
            usdt_collateral = self.client.get_coin_balance(accountType="UNIFIED", coin="USDT")
            if usdt_collateral and usdt_collateral["result"] and usdt_collateral["result"]["balance"]:
                collateral_amount = float(usdt_collateral["result"]["balance"]["walletBalance"])
                return collateral_amount
            else:
                logger.error("ByBit - Failed to retrieve USDT collateral balance. Result structure was unexpected.")
                return 0.0
        except Exception as e:
            logger.error(f"ByBit - Error retrieving available USDT collateral. Error: {e}")
            return 0.0

    def is_already_position_open(self) -> bool:
        try:
            url = "https://api.bybit.com/private/linear/position/list"
            headers = {
                "X-Api-Key": self.api_key,
                "X-Api-Secret": self.api_secret
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                positions = response.json().get('result', [])
                for position in positions:
                    if position.get('size', 0) > 0:
                        return True
                return False
            else:
                logger.error(f"ByBit - Failed to get open positions. HTTP status code: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"ByBit - Error checking if position is open. Error: {e}")
            return False

    
    def test_trade(self):
        self.client.place_order(
            category="linear",
            symbol='ETHUSDT',
            side='Buy',
            orderType="Market",
            qty=1.0,
        )

test = ByBitPositionController()
test.test_trade()