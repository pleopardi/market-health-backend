from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.models import BarSet
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Literal
from .Bar import Bar
from .mappers import bar_set_to_bar_list
from .stock_client import make_stock_client

router = APIRouter(prefix="/bars")


class _QueryParams(BaseModel):
    timeframe: Literal["day", "week"] | None = Field(default="day", title="QueryParams")


@router.get("/{symbol}")
def get_bars(
    symbol: str, params: _QueryParams = Depends(), client=Depends(make_stock_client)
) -> list[Bar] | None:
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
        return bar_set_to_bar_list(result, symbol)

    return None
