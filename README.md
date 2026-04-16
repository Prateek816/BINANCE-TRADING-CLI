# Binance Futures Testnet Trading Bot

A Python CLI application to place **Market** and **Limit** orders on the [Binance Futures Testnet](https://testnet.binancefuture.com) (USDT-M). Built with a clean, layered architecture — separate client, order, and validation modules — with structured logging and full exception handling.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API wrapper (auth, signing, requests)
│   ├── orders.py          # Order placement and response processing
│   ├── validator.py       # Input validation against exchange rules
│   └── logging_config.py  # Logging setup (console + file)
├── cli.py                 # CLI entry point (argparse)
├── .env                   # API credentials (not committed)
├── .env.example           # Template for credentials
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/trading-bot.git
cd trading-bot
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Binance Futures Testnet credentials

1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Register / log in with your GitHub account
3. Navigate to **API Management** and generate your API Key and Secret

### 5. Configure environment variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```env
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
```

> **Never commit your `.env` file.** It is already listed in `.gitignore`.

---

## Usage

### Command syntax

```bash
python3 cli.py <SYMBOL> <SIDE> <TYPE> <QUANTITY> [--price PRICE]
```

| Argument     | Description                          | Example      |
|--------------|--------------------------------------|--------------|
| `SYMBOL`     | Trading pair (case-insensitive)      | `BTCUSDT`    |
| `SIDE`       | Order direction                      | `BUY` / `SELL` |
| `TYPE`       | Order type                           | `MARKET` / `LIMIT` |
| `QUANTITY`   | Amount to trade                      | `0.001`      |
| `--price`    | Limit price — required for LIMIT orders | `30000.0` |

---

## Examples

### Place a MARKET BUY order

```bash
python3 cli.py BTCUSDT BUY MARKET 0.001
```

**Expected output:**

```
--- Order Request Summary ---
Symbol: BTCUSDT
Side:   BUY
Type:   MARKET
Qty:    0.001

✅ Success!
Order ID:     13039712452
Status:       FILLED
Executed Qty: 0.001
Avg Price:    43250.10
```

---

### Place a MARKET SELL order

```bash
python3 cli.py BTCUSDT SELL MARKET 0.001
```

---

### Place a LIMIT BUY order

```bash
python3 cli.py BTCUSDT BUY LIMIT 0.001 --price 30000
```

**Expected output:**

```
--- Order Request Summary ---
Symbol: BTCUSDT
Side:   BUY
Type:   LIMIT
Qty:    0.001
Price:  30000.0

✅ Success!
Order ID:     13039712453
Status:       NEW
Executed Qty: 0.0
Avg Price:    0.00
```

> A LIMIT order with status `NEW` means it has been accepted by the exchange and is waiting to be matched at your specified price.

---

### Place a LIMIT SELL order

```bash
python3 cli.py ETHUSDT SELL LIMIT 0.01 --price 2800
```

---

### Validation error — missing price for LIMIT order

```bash
python3 cli.py BTCUSDT BUY LIMIT 0.001
```

```
❌ Error: Price is required for LIMIT orders.
```

---

### Validation error — invalid symbol

```bash
python3 cli.py INVALIDUSDT BUY MARKET 0.001
```

```
❌ Error: Invalid symbol: INVALIDUSDT. Please use format like 'BTCUSDT'.
```

---

## Logging

All API requests, responses, and errors are logged to `app.log` in the project root.

```
2024-01-15 10:23:41 | INFO  | Fetching exchange info for validation...
2024-01-15 10:23:41 | INFO  | Sending GET request to /fapi/v1/exchangeInfo
2024-01-15 10:23:42 | INFO  | Response from /fapi/v1/exchangeInfo: Success
2024-01-15 10:23:42 | INFO  | Executing MARKET order...
2024-01-15 10:23:42 | INFO  | Sending POST request to /fapi/v1/order
2024-01-15 10:23:42 | INFO  | Response from /fapi/v1/order: Success
```

Logs are written to **both** the console and `app.log` simultaneously.

---

## Requirements

```
requests>=2.31.0
python-dotenv>=1.0.0
```

Install with:

```bash
pip install -r requirements.txt
```

---

## Assumptions

- **Testnet only** — the base URL is hardcoded to `https://testnet.binancefutures.com`. Do not use real API credentials with this bot.
- **One-way position mode** — the bot sends `positionSide: BOTH` on all orders, which is compatible with one-way mode on the testnet. If your account is in hedge mode, switch it to one-way mode in the testnet UI under Futures Settings → Position Mode.
- **USDT-M Futures** — only USDT-margined perpetual contracts are supported (e.g. `BTCUSDT`, `ETHUSDT`).
- **Quantity precision** — quantities are formatted to 3 decimal places (`0.001`) to comply with `LOT_SIZE` filters. If an order is rejected due to precision, check the exchange's `stepSize` for your symbol.
- **Time in Force** — all LIMIT orders use `GTC` (Good Till Cancelled) by default.
- **No leverage management** — the bot does not set or change leverage. Default testnet leverage applies.

---

## Error Handling

| Scenario | Behaviour |
|---|---|
| Missing API credentials | Logs `CRITICAL`, exits with code 1 |
| Invalid symbol | Raises `ValueError` with a clear message |
| Invalid side / order type | Raises `ValueError` with a clear message |
| Non-positive quantity or price | Raises `ValueError` with a clear message |
| Missing price on LIMIT order | Raises `ValueError` with a clear message |
| Network timeout | Logs error, returns failure message |
| Binance API error (4xx/5xx) | Logs raw response, prints failure message |

---

## License

For educational and evaluation purposes only. Not intended for use on live trading accounts.
