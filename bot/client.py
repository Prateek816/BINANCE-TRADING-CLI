import os
from dotenv import load_dotenv
from bot.logging_config import get_logger
import hmac
import hashlib
import time
import requests
import logging
from urllib.parse import urlencode
logger = get_logger(__name__)
load_dotenv()

class BinanceClient:
    def __init__(self, api_key, secret_key):
        self.base_url = "https://testnet.binancefuture.com" 
        self.api_key = api_key
        self.secret_key = secret_key
        self.headers = {"X-MBX-APIKEY": self.api_key}
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

            response.raise_for_status()
            data = response.json()
            
            self.logger.info(f"Response from {endpoint} Sucsess ") 
            return data

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Response Failed , API Request failed: {e}")
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
        """
        Private endpoint for order placement (POST /fapi/v1/order).
        This method is called by orders.py to execute the trade[cite: 31].
        """
        return self._request("POST", "/fapi/v1/order", params=order_params, signed=True)
    
    def get_open_orders(self, symbol):
        return self._request("GET", "/fapi/v1/openOrders", 
                            {"symbol": symbol.upper()}, signed=True)
    
