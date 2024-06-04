from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.models import BarSet
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from typing import Literal
from .Bar import Bar
from .mappers import bar_set_to_bar_list
from .stock_client import make_stock_client


class BarsRepository:
    def __init__(self, client=Depends(make_stock_client)):
        self._client = client

    def get_bars(
        self, symbol: str, timeframe: Literal["day", "week"]
    ) -> list[Bar] | None:
        result = self._client.get_stock_bars(
            StockBarsRequest(
                end=datetime.now() - timedelta(days=1),
                start=datetime.now()
                - (timedelta(days=365) if timeframe == "day" else timedelta(weeks=260)),
                symbol_or_symbols=symbol,
                timeframe=TimeFrame(
                    1,
                    TimeFrameUnit.Day if timeframe == "day" else TimeFrameUnit.Week,
                ),
            )
        )

        if not result[symbol]:
            raise HTTPException(status_code=404, detail="Ticker not found")

        if isinstance(result, BarSet):
            return bar_set_to_bar_list(result, symbol)

        return None
