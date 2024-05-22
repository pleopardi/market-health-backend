from alpaca.data.models import BarSet, Bar as RawBar
from .Bar import Bar


def bar_set_to_bar_list(bar_set: BarSet, symbol: str) -> list[Bar]:
    return list(map(_raw_bar_to_bar, bar_set.data[symbol]))


def _raw_bar_to_bar(raw_bar: RawBar) -> Bar:
    return Bar(
        close=raw_bar.close,
        high=raw_bar.high,
        low=raw_bar.low,
        open=raw_bar.open,
        timestamp=raw_bar.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        volume=raw_bar.volume,
    )
