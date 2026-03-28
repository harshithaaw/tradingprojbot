from bot.log_config import get_logger

log = get_logger("validators") #Creates a logger specifically for this file/module

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
    errors = []

    # symbol check
    if not symbol or not isinstance(symbol, str):
        errors.append("Symbol is required and must be a string e.g. BTCUSDT")
    else:
        symbol = symbol.upper().strip()
        if len(symbol) < 3:
            errors.append(f"Symbol '{symbol}' looks invalid — expected something like BTCUSDT")

    # side check
    if not side:
        errors.append("Side is required — must be BUY or SELL")
    else:
        side = side.upper().strip()
        if side not in VALID_SIDES:
            errors.append(f"Invalid side '{side}' — must be one of {VALID_SIDES}")

    # order type check
    if not order_type:
        errors.append("Order type is required — must be MARKET or LIMIT")
    else:
        order_type = order_type.upper().strip()
        if order_type not in VALID_ORDER_TYPES:
            errors.append(f"Invalid order type '{order_type}' — must be one of {VALID_ORDER_TYPES}")

    # quantity check
    try:
        quantity = float(quantity)
        if quantity <= 0:
            errors.append("Quantity must be a positive number greater than 0")
    except (TypeError, ValueError):
        errors.append(f"Invalid quantity '{quantity}' — must be a number e.g. 0.01")

    # price check — only required for LIMIT orders
    if order_type == "LIMIT":
        if price is None:
            errors.append("Price is required for LIMIT orders")
        else:
            try:
                price = float(price)
                if price <= 0:
                    errors.append("Price must be a positive number greater than 0")
            except (TypeError, ValueError):
                errors.append(f"Invalid price '{price}' — must be a number e.g. 50000")

    if errors:
        for e in errors:
            log.warning("Validation failed: %s", e)
        raise ValueError("\n".join(errors))

    log.info("Validation passed — symbol=%s side=%s type=%s qty=%s price=%s",
             symbol, side, order_type, quantity, price)

    return {
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "price": price
    }