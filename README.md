```bash
trading_bot/
[cite_start]├── cli.py              # Application entry point and CLI layer
├── bot/
│    ├── __init__.py     # Package initialization
|    ├── client.py       # Binance API wrapper and authentication 
|    ├── orders.py       # Order execution and formatting logic
|    ├── validator.py    # Input and exchange rule validation 
|    └── logging_config.py # Logging setup and configuration 
├── .env                # API Keys (not tracked by git)
└── requirements.txt    # Project dependencies
'''
