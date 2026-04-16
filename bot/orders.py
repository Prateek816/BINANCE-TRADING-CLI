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
        "quantity": quantity,
        "positionSide": "BOTH"
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
    if "error" in response:
        return {"success": False, "message": f"Order Failed: {response.get('message')}"}

    # Extract raw values
    exec_qty = float(response.get("executedQty", 0))
    cum_quote = float(response.get("cumQuote", 0))
    
    # Calculate Avg Price if avgPrice field is "0.00" or missing
    avg_price = response.get("avgPrice")
    if (not avg_price or float(avg_price) == 0) and exec_qty > 0:
        avg_price = f"{cum_quote / exec_qty:.2f}"
    elif not avg_price:
        avg_price = "0.00"

    return {
        "success": True,
        "orderId": response.get("orderId"),
        "status": response.get("status"),
        "executedQty": f"{exec_qty:.4f}",
        "avgPrice": avg_price
    }