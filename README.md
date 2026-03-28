# tradingprojbot

A command-line trading bot that places orders on Binance Futures Testnet (USDT-M).
Built with Python using direct REST calls — no third-party Binance SDK.

---

## Project Structure
```
tradingprojbot/
├── bot/
│   ├── client.py         # Binance API wrapper — handles auth, signing, HTTP
│   ├── order.py          # Order placement logic
│   ├── validators.py     # Input validation and sanitization
│   └── log_config.py     # Logging setup — writes to file and terminal
├── cli.py                # CLI entry point
├── .env.example          # Environment variable template
├── requirements.txt
└── README.md
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/tradingprojbot.git
cd tradingprojbot
```

**2. Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

Get your API keys from [Binance Futures Testnet](https://testnet.binancefuture.com)
```
API_KEY=your_api_key_here
API_SECRET=your_secret_key_here
BASE_URL=https://testnet.binancefuture.com
```

---

## How to Run

**Market Order — Buy**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.01
```

**Market Order — Sell**
```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --qty 0.01
```

**Limit Order — Buy**
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --qty 0.01 --price 80000
```

**Limit Order — Sell**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.01 --price 99000
```

**Show help**
```bash
python cli.py --help
```

---

## Example Output
```
========== ORDER REQUEST ==========
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
===================================

========== ORDER RESULT ==========
  Order ID     : 13001983395
  Symbol       : BTCUSDT
  Side         : BUY
  Type         : MARKET
  Status       : NEW
  Quantity     : 0.010
  Executed Qty : 0.000
  Avg Price    : 0.00
  Price        : 0.00
==================================

✅ Order placed successfully!
```

---

## Logging

All API requests, responses, and errors are logged automatically to the `logs/` folder.
Each run creates a new timestamped log file e.g. `logs/bot_20260328_170000.log`

Log levels:
- `INFO` — normal operations, order placed, validation passed
- `WARNING` — validation failures, bad input
- `ERROR` — API errors, network failures

---

## Assumptions

- Testnet only — base URL is hardcoded to `https://testnet.binancefuture.com`
- Quantity precision depends on the symbol — for BTCUSDT minimum is 0.001
- LIMIT orders use `timeInForce=GTC` (Good Till Cancelled) by default
- API keys are stored in `.env` and never committed to version control

---

## Requirements

- Python 3.8+
- Binance Futures Testnet account and API credentials