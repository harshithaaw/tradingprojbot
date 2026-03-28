from bot.client import BinanceClient
from bot.validators import validate_order
from bot.log_config import get_logger

log = get_logger("orders")
client = BinanceClient()


def place_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:

    # step 1 — validate everything first
    validated = validate_order(symbol, side, order_type, quantity, price)

    # step 2 — build params Binance expects
    params = {
        "symbol":   validated["symbol"],
        "side":     validated["side"],
        "type":     validated["order_type"],
        "quantity": validated["quantity"],
    }

    # LIMIT orders need price and timeInForce
    if validated["order_type"] == "LIMIT":
        params["price"] = validated["price"]
        params["timeInForce"] = "GTC"  # Good Till Cancelled

    log.info("Sending order to Binance — %s", params)

    # step 3 — send to Binance via client
    response = client.place_order(**params)

    log.info("Order response — orderId=%s status=%s", response.get("orderId"), response.get("status"))

    return response


def format_response(response: dict) -> str:
    lines = [
        "\n========== ORDER RESULT ==========",
        f"  Order ID     : {response.get('orderId', 'N/A')}",
        f"  Symbol       : {response.get('symbol', 'N/A')}",
        f"  Side         : {response.get('side', 'N/A')}",
        f"  Type         : {response.get('type', 'N/A')}",
        f"  Status       : {response.get('status', 'N/A')}",
        f"  Quantity     : {response.get('origQty', 'N/A')}",
        f"  Executed Qty : {response.get('executedQty', 'N/A')}",
        f"  Avg Price    : {response.get('avgPrice', 'N/A')}",
        f"  Price        : {response.get('price', 'N/A')}",
        "==================================\n"
    ]
    return "\n".join(lines)