import logging
from bot.logging_config import get_logger
logger = get_logger(__name__)

def execute_order(client, symbol, side, order_type, quantity, price=None):
    """
    Coordinates with BinanceClient to place MARKET or LIMIT orders.
    Maps CLI inputs to the specific dictionary keys required by the API.
    """
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity
    }

    if order_type.upper() == "LIMIT":
        if price is None:
            return {"error": True, "message": "Price is required for LIMIT orders"}
        params["price"] = price
        params["timeInForce"] = "GTC" 

    logger.info(f"Preparing {order_type} {side} order for {symbol}")

    response = client.place_order(params)

    return process_order_response(response)

def process_order_response(response):
    """
    Extracts specific details from the Binance API response for the CLI output.
    """
    if "error" in response:
        return {
            "success": False,
            "message": f"Order Failed: {response.get('message')}"
        }

    order_data = {
        "success": True,
        "orderId": response.get("orderId"),
        "status": response.get("status"),
        "executedQty": response.get("executedQty"),
        "avgPrice": response.get("avgPrice", "0.00"), 
        "symbol": response.get("symbol"),
        "side": response.get("side"),
        "type": response.get("type")
    }
    
    return order_data