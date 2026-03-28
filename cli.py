# It needs to:
# Accept arguments from the terminal
# Call validators and orders
# Print clean readable output
# Handle any crash gracefully so the user sees a helpful message, not a Python traceback

import argparse  #lets you pass inputs from terminal (CLI)
import sys
from bot.order import place_order, format_response #makes API response readable
from bot.log_config import get_logger

log = get_logger("cli")


def build_parser() -> argparse.ArgumentParser:             #This function defines what inputs your program accepts
    parser = argparse.ArgumentParser(
        prog="tradingbot",
        description="Binance Futures Testnet — Order Placement CLI",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
examples:
  Market Buy:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.01

  Limit Sell:
    python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.01 --price 80000

        """
    )

    parser.add_argument("--symbol",   required=True,  help="Trading pair e.g. BTCUSDT")
    parser.add_argument("--side",     required=True,  help="BUY or SELL")
    parser.add_argument("--type",     required=True,  help="MARKET, LIMIT, or STOP_MARKET", dest="order_type")
    parser.add_argument("--qty",      required=True,  help="Order quantity e.g. 0.01", type=float)
    parser.add_argument("--price",    required=False, help="Price — required for LIMIT ", type=float, default=None)

    return parser


def print_request_summary(args):
    print("\n========== ORDER REQUEST ==========")
    print(f"  Symbol     : {args.symbol.upper()}")
    print(f"  Side       : {args.side.upper()}")
    print(f"  Type       : {args.order_type.upper()}")
    print(f"  Quantity   : {args.qty}")
    if args.price:
        print(f"  Price      : {args.price}")
    print("===================================\n")


def main():
    parser = build_parser()
    args = parser.parse_args()  #Converts command-line input into args object

    log.info("CLI started — args: symbol=%s side=%s type=%s qty=%s price=%s",
             args.symbol, args.side, args.order_type, args.qty, args.price)

    print_request_summary(args)

    try:
        response = place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.qty,
            price=args.price
        )

        print(format_response(response))
        print("✅ Order placed successfully!")
        log.info("Order placed successfully — orderId=%s", response.get("orderId"))

    except ValueError as e:
        print(f"\n❌ Validation Error:\n{e}")
        log.warning("Validation error: %s", e)
        sys.exit(1)

    except RuntimeError as e:
        print(f"\n❌ API Error:\n{e}")
        log.error("API error: %s", e)
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        log.exception("Unexpected error occurred")
        sys.exit(1)


if __name__ == "__main__":
    main()