from GlobalUtils.globalUtils import *
from GlobalUtils.logger import *
from pubsub import pub
from PositionMonitor.Master.MasterPositionMonitorUtils import *
from TxExecution.HMX.HMXPositionControllerUtils import *
import sqlite3
from GlobalUtils.globalUtils import GLOBAL_HMX_CLIENT

class HMXPositionMonitor():
    def __init__(self, db_path='trades.db'):
        self.client = GLOBAL_HMX_CLIENT
        self.db_path = db_path
        try:
            self.conn = sqlite3.connect(self.db_path)
        except Exception as e:
            logger.error(f"HMXPositionMonitor - Error accessing the database: {e}")
            return None

    def get_open_position(self) -> dict:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT * FROM trade_log WHERE open_close = 'Open' AND exchange = 'Synthetix';''')
                open_positions = cursor.fetchall()
                if open_positions:
                    position_dict = get_dict_from_database_response(open_positions[0])
                    return position_dict
                else:
                    return None
        except Exception as e:
            logger.error(f"HMXPositionMonitor - Error while searching for open HMX positions: {e}")
            return None

    def is_near_liquidation_price(self, position: dict) -> bool:
        try:
            percentage_from_liqiudation_price = get_percentage_away_from_liquidation_price(position)
            MAX_ALLOWABLE_PERCENTAGE_AWAY_FROM_LIQUIDATION_PRICE = float(os.getenv('MAX_ALLOWABLE_PERCENTAGE_AWAY_FROM_LIQUIDATION_PRICE'))
            if percentage_from_liqiudation_price < MAX_ALLOWABLE_PERCENTAGE_AWAY_FROM_LIQUIDATION_PRICE:
                logger.info(f'HMXPositionMonitor - Liquidation risk detected for position, percentage_from_liqiudation_price = {percentage_from_liqiudation_price}, MAX_ALLOWABLE_PERCENTAGE_AWAY_FROM_LIQUIDATION_PRICE = {MAX_ALLOWABLE_PERCENTAGE_AWAY_FROM_LIQUIDATION_PRICE}')
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"HMXPositionMonitor - Error checking if near liquidation price for HMX position: {position}: Error: {e}")
            return False


    def get_funding_rate(self, position: dict) -> float:
        try:
            symbol = position['symbol']
            market_id = get_market_for_symbol(symbol)
            market_data = self.client.public.get_market_info(market_id)
            funding_rate = float(market_data['funding_rate']['8H'])
            return funding_rate
            
        except Exception as e:
            logger.error(f"HMXPositionMonitor - Error fetching funding rate for symbol {symbol}: {e}")
            return None

    def is_open_position(self) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT * FROM trade_log WHERE open_close = 'Open' AND exchange = 'HMX';''')
                open_positions = cursor.fetchall()
                if open_positions:
                    return True
                else:
                    return False
        except Exception as e:
            logger.error(f"HMXPositionMonitor - Error while searching for open HMX positions:", {e})
            return None

