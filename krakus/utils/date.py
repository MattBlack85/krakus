from datetime import datetime


def convert_ts_to_dt(ts: str) -> datetime:
    return datetime.fromtimestamp(int(ts))
