from bot.logging_config import get_logger

logger = get_logger(__name__)

class Validator:
    def __init__(self, exchange_info):
        """
        Initializes with exchange metadata to validate against real-time rules.
        """
        self.exchange_info = exchange_info

    def validate_symbol(self, symbol):
        """Checks if the symbol exists on Binance Futures Testnet[cite: 21]."""
        symbols = [s['symbol'] for s in self.exchange_info.get('symbols', [])]
        if symbol.upper() not in symbols:
            raise ValueError(f"Invalid symbol: {symbol}. Please use format like 'BTCUSDT'[cite: 21].")
        return symbol.upper()

    def validate_side(self, side):
        """Ensures side is either BUY or SELL[."""
        if side.upper() not in ["BUY", "SELL"]:
            raise ValueError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'.")
        return side.upper()

    def validate_order_type(self, order_type):
        """Ensures order type is MARKET or LIMIT."""
        if order_type.upper() not in ["MARKET", "LIMIT"]:
            raise ValueError(f"Invalid order type: {order_type}. Must be 'MARKET' or 'LIMIT'.")
        return order_type.upper()

    def validate_quantity(self, quantity):
        """Ensures quantity is a positive number]."""
        try:
            q = float(quantity)
            if q <= 0:
                raise ValueError("Quantity must be greater than 0.")
            return q
        except (ValueError, TypeError):
            raise ValueError(f"Invalid quantity: {quantity}. Must be a numeric value.")

    def validate_price(self, order_type, price):
        """Ensures price is provided and valid for LIMIT orders."""
        if order_type.upper() == "LIMIT":
            if price is None or str(price).strip() == "":
                raise ValueError("Price is required for LIMIT orders.")
            try:
                p = float(price)
                if p <= 0:
                    raise ValueError("Price must be greater than 0.")
                return p
            except (ValueError, TypeError):
                raise ValueError(f"Invalid price: {price}. Must be a numeric value.")
        return None

    def validate_all(self, symbol, side, order_type, quantity, price=None):
        """
        Runs all basic validations and returns cleaned data.
        Fulfills 'Accept and validate user input' requirement.
        """
        validated_data = {
            "symbol": self.validate_symbol(symbol),
            "side": self.validate_side(side),
            "order_type": self.validate_order_type(order_type),
            "quantity": self.validate_quantity(quantity),
            "price": self.validate_price(order_type, price)
        }
        return validated_data