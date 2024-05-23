from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Literal
from .Bar import Bar
from .repository import BarsRepository

router = APIRouter(prefix="/bars")


class _QueryParams(BaseModel):
    timeframe: Literal["day", "week"] | None = Field(default="day", title="QueryParams")


@router.get("/{symbol}")
def get_bars(
    symbol: str,
    params: _QueryParams = Depends(),
    repository=Depends(BarsRepository),
) -> list[Bar] | None:
    return repository.get_bars(symbol, params.model_dump().get("timeframe"))
