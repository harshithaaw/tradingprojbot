from bot.validators import validate_order

# Test 1 — valid market order
print("Test 1 — valid MARKET order")
result = validate_order("BTCUSDT", "BUY", "MARKET", 0.01)
print("Passed:", result)

# Test 2 — limit order missing price
print("\nTest 2 — LIMIT order missing price")
try:
    validate_order("BTCUSDT", "BUY", "LIMIT", 0.01)
except ValueError as e:
    print("Caught expected error:", e)

# Test 3 — bad side
print("\nTest 3 — bad side value")
try:
    validate_order("BTCUSDT", "BUYYY", "MARKET", 0.01)
except ValueError as e:
    print("Caught expected error:", e)

# Test 4 — negative quantity
print("\nTest 4 — negative quantity")
try:
    validate_order("BTCUSDT", "SELL", "MARKET", -5)
except ValueError as e:
    print("Caught expected error:", e)