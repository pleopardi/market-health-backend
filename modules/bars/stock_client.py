from alpaca.data.historical import StockHistoricalDataClient
from os import environ


def make_stock_client():
    return StockHistoricalDataClient(
        environ.get("ALPACA_API_KEY"), environ.get("ALPACA_SECRET_KEY")
    )
