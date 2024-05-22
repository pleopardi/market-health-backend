from pydantic import BaseModel


class Bar(BaseModel):
    close: float
    high: float
    low: float
    open: float
    timestamp: str
    volume: float
