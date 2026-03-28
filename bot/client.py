# This is the only file in your entire project that talks to Binance.
#  Every API call, every HTTP request, every signature happens here and nowhere else.

import hashlib
import hmac
import time
import os
import requests                            #requests → send HTTP requests (talk to Binance API)
from urllib.parse import urlencode         #urlencode → convert dicts to URL query strings
from dotenv import load_dotenv             #load_dotenv → load variables from .env
from bot.log_config import get_logger      #get_logger → get logger instance

load_dotenv()
log = get_logger("client")

class BinanceClient:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        self.base_url = os.getenv("BASE_URL", "https://testnet.binancefuture.com")

        if not self.api_key or not self.api_secret:
            raise ValueError("API_KEY and API_SECRET must be set in your .env file")

        self.session = requests.Session()    #Reuses connection (faster)
        self.session.headers.update({        #Adds headers automatically to every request
            "X-MBX-APIKEY": self.api_key,      
            "Content-Type": "application/x-www-form-urlencoded"
        })
        log.info("BinanceClient initialized — connected to %s", self.base_url)

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)   #Adds current time (required by Binance)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    #sends req safely
    def _post(self, endpoint: str, params: dict) -> dict:
        signed = self._sign(params)
        url = f"{self.base_url}{endpoint}"

        log.debug("POST %s | params: %s", url, {k: v for k, v in signed.items() if k != "signature"})

        try:
            response = self.session.post(url, data=signed)
            data = response.json()

            if response.status_code != 200:
                log.error("API error %s: %s", response.status_code, data)
                raise RuntimeError(f"Binance API error: {data.get('msg', 'Unknown error')} (code {data.get('code')})")

            log.debug("Response: %s", data)
            return data

        except requests.exceptions.ConnectionError:
            log.error("Network error — could not reach Binance testnet")
            raise RuntimeError("Network error — check your internet connection")

        except requests.exceptions.Timeout:
            log.error("Request timed out")
            raise RuntimeError("Request timed out — Binance did not respond")

    #place order
    def place_order(self, **kwargs) -> dict:
        log.info("Placing order: %s", kwargs)
        return self._post("/fapi/v1/order", kwargs)
#         Accepts flexible parameters like:
            # client.place_order(
            #     symbol="BTCUSDT",
            #     side="BUY",
            #     type="MARKET",
            #     quantity=0.01
            # )



# 1. Take all your parameters (symbol, side, qty etc.)
# 2. Add a timestamp
# 3. Hash them with your secret key → gives you a "signature"
# 4. Send everything + signature to Binance
# 5. Binance re-hashes on their end → if it matches, request is valid