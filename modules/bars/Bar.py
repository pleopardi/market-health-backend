from pydantic import BaseModel


class Bar(BaseModel):
    close: float
    high: float
    low: float
    open: float
    time: str
    volume: float
