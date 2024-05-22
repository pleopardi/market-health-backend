from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.models import BarSet, Bar as RawBar
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from os import environ
from pydantic import BaseModel, Field
from typing import Literal

router = APIRouter(prefix="/bars")

client = StockHistoricalDataClient(
    environ.get("ALPACA_API_KEY"), environ.get("ALPACA_SECRET_KEY")
)


class Bar(BaseModel):
    close: float
    high: float
    low: float
    open: float
    timestamp: str
    volume: float


def BarSet_to_BarList(bar_set: BarSet, symbol: str) -> list[Bar]:
    return list(map(RawBar_to_Bar, bar_set.data[symbol]))


def RawBar_to_Bar(raw_bar: RawBar) -> Bar:
    return Bar(
        close=raw_bar.close,
        high=raw_bar.high,
        low=raw_bar.low,
        open=raw_bar.open,
        timestamp=raw_bar.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        volume=raw_bar.volume,
    )


class QueryParams(BaseModel):
    timeframe: Literal["day", "week"] | None = Field(default="day", title="QueryParams")


@router.get("/{symbol}")
def get_bars(symbol: str, params: QueryParams = Depends()) -> list[Bar] | None:
    print(params.model_dump().get("timeframe"))
    result = client.get_stock_bars(
        StockBarsRequest(
            end=datetime.now() - timedelta(days=1),
            start=datetime.now()
            - (
                timedelta(days=365)
                if params.model_dump().get("timeframe") == "day"
                else timedelta(weeks=260)
            ),
            symbol_or_symbols=symbol,
            timeframe=TimeFrame(
                1,
                TimeFrameUnit.Day
                if params.model_dump().get("timeframe") == "day"
                else TimeFrameUnit.Week,
            ),
        )
    )

    if isinstance(result, BarSet):
        return BarSet_to_BarList(result, symbol)

    return None
