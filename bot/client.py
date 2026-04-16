import os
from binance import Client
from dotenv import load_dotenv
import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
from binance.exceptions import BinanceAPIException
from bot.logging_config import setup_logging

setup_logging(level="DEBUG", log_file="app.log") # see about logging part


load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")



import hmac
import hashlib
import time
import requests
import logging
from urllib.parse import urlencode

# Note: In a real scenario, use environment variables for keys
class BinanceClient:
    def __init__(self, api_key, secret_key):
        self.base_url = "https://testnet.binancefuture.com" 
        self.api_key = api_key
        self.secret_key = secret_key
        self.headers = {"X-MBX-APIKEY": self.api_key}
        # Logging should be configured in logging_config.py as per instructions [cite: 56]
        self.logger = logging.getLogger(__name__)

    def _generate_signature(self, params):
        """Generates HMAC SHA256 signature[cite: 14, 32]."""
        query_string = urlencode(params)
        return hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _request(self, method, endpoint, params=None, signed=False):
        """Unified request handler with logging and error handling[cite: 31, 32]."""
        url = f"{self.base_url}{endpoint}"
        
        if params is None:
            params = {}

        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)

        try:
            self.logger.info(f"Sending {method} request to {endpoint} with params: {params}") 
            
            if method.upper() == "GET":
                response = requests.get(url, params=params, headers=self.headers, timeout=10)
            else:
                response = requests.post(url, params=params, headers=self.headers, timeout=10)

            # Check for HTTP errors 
            response.raise_for_status()
            data = response.json()
            
            self.logger.info(f"Response from {endpoint}: {data}") 
            return data

        except requests.exceptions.RequestException as e:
            self.logger.error(f"API Request failed: {e}")
            # Providing clear failure messages as required [cite: 29]
            if hasattr(e.response, 'json'):
                return {"error": True, "message": e.response.json()}
            return {"error": True, "message": str(e)}

    def get_exchange_info(self):
        """Public endpoint to validate symbols/filters[cite: 63]."""
        return self._request("GET", "/fapi/v1/exchangeInfo")

    def get_ticker_price(self, symbol):
        """Public endpoint for current market price."""
        return self._request("GET", "/fapi/v1/ticker/price", {"symbol": symbol.upper()})

    def get_account_balance(self):
        """Private endpoint to check USDT balance[cite: 23]."""
        return self._request("GET", "/fapi/v2/account", signed=True)

    def place_order(self, order_params):
        """Private endpoint for order placement[cite: 18]."""
        return self._request("POST", "/fapi/v1/order", params=order_params, signed=True)