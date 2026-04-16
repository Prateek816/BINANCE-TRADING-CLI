import argparse
import sys
from bot.client import BinanceClient
from bot.orders import execute_order
from bot.validator import Validator
from bot.logging_config import setup_logging, get_logger

# 1. Initialize Logging
setup_logging()
logger = get_logger(__name__)
from dotenv import load_dotenv
import os
load_dotenv()

def main():
    # 2. Setup CLI Arguments 
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("symbol", type=str, help="e.g., BTCUSDT") 
    parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="BUY or SELL") 
    parser.add_argument("type", type=str, choices=["MARKET", "LIMIT"], help="MARKET or LIMIT")
    parser.add_argument("quantity", type=float, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price (required for LIMIT orders)") 

    args = parser.parse_args()

    # 3. Initialize API Client (Replace with your keys/env vars)
    # Using Testnet Base URL: https://testnet.binancefuture.com [cite: 10, 11]
    client = BinanceClient(api_key = os.environ['BINANCE_API_KEY'],secret_key = os.environ['BINANCE_SECRET_KEY'])

    try:
        # 4. Input Validation [cite: 20, 32]
        logger.info("Fetching exchange info for validation...")
        exchange_info = client.get_exchange_info()
        validator = Validator(exchange_info)
        
        # This will raise a ValueError if validation fails 
        clean_data = validator.validate_all(
            args.symbol, args.side, args.type, args.quantity, args.price
        )

        # 5. Print Order Request Summary [cite: 28]
        print("\n--- Order Request Summary ---")
        print(f"Symbol: {clean_data['symbol']}")
        print(f"Side:   {clean_data['side']}")
        print(f"Type:   {clean_data['order_type']}")
        print(f"Qty:    {clean_data['quantity']}")
        if clean_data['price']:
            print(f"Price:  {clean_data['price']}")

        # 6. Execute Order
        logger.info(f"Executing {clean_data['order_type']} order...")
        result = execute_order(
            client, 
            clean_data['symbol'], 
            clean_data['side'], 
            clean_data['order_type'], 
            clean_data['quantity'], 
            clean_data['price']
        )

        # 7. Print Response Details & Success/Failure [cite: 29]
        if result.get("success"):
            print("\n✅ Success!")
            print(f"Order ID:     {result['orderId']}")
            print(f"Status:       {result['status']}")
            print(f"Executed Qty: {result['executedQty']}")
            print(f"Avg Price:    {result['avgPrice']}")
        else:
            print(f"\n❌ Failure: {result.get('message')}")

    except Exception as e:
        logger.error(f"Application Error: {e}") 
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()