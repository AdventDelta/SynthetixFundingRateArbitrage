from TxExecution.Synthetix.SynthetixPositionController import SynthetixPositionController
import argparse

def run(args):
    x = SynthetixPositionController()
    x.check_for_accounts()
    x.approve_and_deposit_collateral(token_address=args.token_address, amount=args.token_amount)

def main():
    parser = argparse.ArgumentParser(description="Approve and deposit collateral using the SynthetixPositionController")
    parser.add_argument('token_address', type=str, help='The address of the token to deposit')
    parser.add_argument('token_amount', type=int, help='The amount of the token to deposit (in token decimals)')
    args = parser.parse_args()
    run(args)
