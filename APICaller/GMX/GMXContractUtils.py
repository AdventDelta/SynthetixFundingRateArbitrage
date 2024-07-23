from gmx_python_sdk.scripts.v2.gmx_utils import *
from gmx_python_sdk.scripts.v2.get.get import GetData
from gmx_python_sdk.scripts.v2.get.get_open_interest import OpenInterest
from APICaller.GMX.GMXCallerUtils import ARBITRUM_CONFIG_OBJECT

DATASTORE_CONTRACT_OBJECT = get_datastore_contract(ARBITRUM_CONFIG_OBJECT)
READER_CONTRACT_OBJECT = get_reader_contract(ARBITRUM_CONFIG_OBJECT)

FUNDING_FACTOR = create_hash_string("FUNDING_FACTOR")
FUNDING_EXPONENT_FACTOR = create_hash_string("FUNDING_EXPONENT_FACTOR")
FUNDING_INCREASE_FACTOR_PER_SECOND = create_hash_string("FUNDING_INCREASE_FACTOR_PER_SECOND")
FUNDING_DECREASE_FACTOR_PER_SECOND = create_hash_string("FUNDING_DECREASE_FACTOR_PER_SECOND")
MIN_FUNDING_FACTOR_PER_SECOND_LIMIT = create_hash_string("MIN_FUNDING_FACTOR_PER_SECOND_LIMIT")
MAX_FUNDING_FACTOR_PER_SECOND_LIMIT = create_hash_string("MAX_FUNDING_FACTOR_PER_SECOND_LIMIT")
THRESHOLD_FOR_STABLE_FUNDING = create_hash_string("THRESHOLD_FOR_STABLE_FUNDING")
THRESHOLD_FOR_DECREASE_FUNDING = create_hash_string("THRESHOLD_FOR_DECREASE_FUNDING")

OPTIMAL_USAGE_FACTOR = create_hash_string("OPTIMAL_USAGE_FACTOR")
BASE_BORROWING_FACTOR = create_hash_string("BASE_BORROWING_FACTOR")
BELOW_OPTIMAL_USAGE_BORROWING_FACTOR = create_hash_string("BELOW_OPTIMAL_USAGE_BORROWING_FACTOR")
BORROWING_FACTOR = create_hash_string("BORROWING_FACTOR")
BORROWING_EXPONENT_FACTOR = create_hash_string("BORROWING_EXPONENT_FACTOR") 

ACCOUNT_POSITION_LIST = create_hash_string("ACCOUNT_POSITION_LIST")
CLAIMABLE_FEE_AMOUNT = create_hash_string("CLAIMABLE_FEE_AMOUNT")
DECREASE_ORDER_GAS_LIMIT = create_hash_string("DECREASE_ORDER_GAS_LIMIT")
DEPOSIT_GAS_LIMIT = create_hash_string("DEPOSIT_GAS_LIMIT")

WITHDRAWAL_GAS_LIMIT = create_hash_string("WITHDRAWAL_GAS_LIMIT")

EXECUTION_GAS_FEE_BASE_AMOUNT = create_hash_string("EXECUTION_GAS_FEE_BASE_AMOUNT")
EXECUTION_GAS_FEE_MULTIPLIER_FACTOR = create_hash_string("EXECUTION_GAS_FEE_MULTIPLIER_FACTOR")
INCREASE_ORDER_GAS_LIMIT = create_hash_string("INCREASE_ORDER_GAS_LIMIT")
MAX_OPEN_INTEREST = create_hash_string("MAX_OPEN_INTEREST")
MAX_PNL_FACTOR_FOR_TRADERS = create_hash_string("MAX_PNL_FACTOR_FOR_TRADERS")
MAX_PNL_FACTOR_FOR_DEPOSITS = create_hash_string("MAX_PNL_FACTOR_FOR_DEPOSITS")
MAX_PNL_FACTOR_FOR_WITHDRAWALS = create_hash_string("MAX_PNL_FACTOR_FOR_WITHDRAWALS")
MIN_ADDITIONAL_GAS_FOR_EXECUTION = create_hash_string("MIN_ADDITIONAL_GAS_FOR_EXECUTION")
OPEN_INTEREST_IN_TOKENS = create_hash_string("OPEN_INTEREST_IN_TOKENS")
OPEN_INTEREST = create_hash_string("OPEN_INTEREST")
OPEN_INTEREST_RESERVE_FACTOR = create_hash_string(
    "OPEN_INTEREST_RESERVE_FACTOR"
)
POOL_AMOUNT = create_hash_string("POOL_AMOUNT")
RESERVE_FACTOR = create_hash_string("RESERVE_FACTOR")
SINGLE_SWAP_GAS_LIMIT = create_hash_string("SINGLE_SWAP_GAS_LIMIT")
SWAP_ORDER_GAS_LIMIT = create_hash_string("SWAP_ORDER_GAS_LIMIT")
VIRTUAL_TOKEN_ID = create_hash_string("VIRTUAL_TOKEN_ID")

MIN_COLLATERAL_FACTOR = create_hash_string("MIN_COLLATERAL_FACTOR")
MIN_COLLATERAL_USD = create_hash_string("MIN_COLLATERAL_USD")
MIN_POSITION_SIZE_USD = create_hash_string("MIN_POSITION_SIZE_USD")


def minCollateralFactorKey(market: str):
    return create_hash(["bytes32", "address"], [MIN_COLLATERAL_FACTOR, market])

def minCollateralUsdKey(market: str):
    return create_hash(["bytes32", "address"], [MIN_COLLATERAL_FACTOR, market])

def accountPositionListKey(account):
    return create_hash(
        ["bytes32", "address"],
        [ACCOUNT_POSITION_LIST, account]
    )


def claimable_fee_amount_key(market: str, token: str):
    return create_hash(
        ["bytes32", "address", "address"],
        [CLAIMABLE_FEE_AMOUNT, market, token]
    )


def decrease_order_gas_limit_key():
    return DECREASE_ORDER_GAS_LIMIT


def deposit_gas_limit_key():
    return DEPOSIT_GAS_LIMIT


def execution_gas_fee_base_amount_key():
    return EXECUTION_GAS_FEE_BASE_AMOUNT


def execution_gas_fee_multiplier_key():
    return EXECUTION_GAS_FEE_MULTIPLIER_FACTOR


def increase_order_gas_limit_key():
    return INCREASE_ORDER_GAS_LIMIT


def min_additional_gas_for_execution_key():
    return MIN_ADDITIONAL_GAS_FOR_EXECUTION


def max_open_interest_key(market: str,
                          is_long: bool):

    return create_hash(
        ["bytes32", "address", "bool"],
        [MAX_OPEN_INTEREST, market, is_long]
    )


def open_interest_in_tokens_key(
    market: str,
    collateral_token: str,
    is_long: bool
):
    return create_hash(
        ["bytes32", "address", "address", "bool"],
        [OPEN_INTEREST_IN_TOKENS, market, collateral_token, is_long]
    )


def open_interest_key(
    market: str,
    collateral_token: str,
    is_long: bool
):
    return create_hash(
        ["bytes32", "address", "address", "bool"],
        [OPEN_INTEREST, market, collateral_token, is_long]
    )


def open_interest_reserve_factor_key(
    market: str,
    is_long: bool
):
    return create_hash(
        ["bytes32", "address", "bool"],
        [OPEN_INTEREST_RESERVE_FACTOR, market, is_long]
    )


def pool_amount_key(
    market: str,
    token: str
):
    return create_hash(
        ["bytes32", "address", "address"],
        [POOL_AMOUNT, market, token]
    )


def reserve_factor_key(
    market: str,
    is_long: bool
):
    return create_hash(
        ["bytes32", "address", "bool"],
        [RESERVE_FACTOR, market, is_long]
    )


def single_swap_gas_limit_key():
    return SINGLE_SWAP_GAS_LIMIT


def swap_order_gas_limit_key():
    return SWAP_ORDER_GAS_LIMIT


def virtualTokenIdKey(token: str):
    return create_hash(["bytes32", "address"], [VIRTUAL_TOKEN_ID, token])


def withdraw_gas_limit_key():
    return WITHDRAWAL_GAS_LIMIT


class GetFundingCalculationData(GetData):
    def __init__(self, config):
        super().__init__(config)
        self.config = config

    def _get_data_processing(self):

        open_interest = OpenInterest(
            config=self.config
        ).get_data(to_json=False)


        # define empty lists to pass to zip iterater later on
        mapper = []
        output_list = []
        long_interest_usd_list = []
        short_interest_usd_list = []

        # loop markets
        for market_key in self.markets.info:
            symbol = self.markets.get_market_symbol(market_key)
            index_token_address = self.markets.get_index_token_address(
                market_key
            )
            self._get_token_addresses(market_key)

            output = self._get_oracle_prices(
                market_key,
                index_token_address,
            )

            mapper.append(symbol)
            output_list.append(output)
            long_interest_usd_list = (
                long_interest_usd_list +
                [
                    open_interest['long'][symbol] * 10 ** 30
                ]
            )
            short_interest_usd_list = (
                short_interest_usd_list +
                [
                    open_interest['short'][symbol] * 10 ** 30
                ]
            )

        # Multithreaded call on contract
        threaded_output = execute_threading(output_list)
        for (
            output,
            long_interest_usd,
            short_interest_usd,
            symbol
        ) in zip(
            threaded_output,
            long_interest_usd_list,
            short_interest_usd_list,
            mapper
        ):

            market_info_dict = {
                "market_token": output[0][0],
                "index_token": output[0][1],
                "long_token": output[0][2],
                "short_token": output[0][3],
                "long_borrow_fee": output[1],
                "short_borrow_fee": output[2],
                "is_long_pays_short": output[4][0],
                "funding_factor_per_second": output[4][1]
            }

            long_funding_fee = get_funding_factor_per_period(
                market_info_dict,
                True,
                3600 * 8,
                long_interest_usd,
                short_interest_usd
            )

            short_funding_fee = get_funding_factor_per_period(
                market_info_dict,
                False,
                3600 * 8,
                long_interest_usd,
                short_interest_usd
            )

            self.output['long'][symbol] = long_funding_fee
            self.output['short'][symbol] = short_funding_fee

        return self.output

reader = READER_CONTRACT_OBJECT
x = reader.functions['']