# workspace\tools\time\time_helper.py
from datetime import datetime, timedelta, timezone

def date_to_timestamp(date: datetime, tz: timezone = timezone.utc) -> int:
    """
    將 datetime 轉換成秒級 timestamp
    :param date: datetime 物件
    :param tz: datetime 所屬的時區 (預設 UTC)
    :return: int (timestamp, 秒級)
    """
    return int(date.replace(tzinfo=tz).timestamp())


def day_range(date: datetime, tz: timezone = timezone.utc) -> tuple[int, int]:
    """
    給一個日期，回傳該日期在指定時區的起點/終點對應的 UTC timestamp
    :param date: datetime 物件 (通常是日期，不含時間)
    :param tz: 指定時區，例如 timezone.utc 或 timezone(timedelta(hours=8)) (台灣)
    :return: (start_ts, end_ts)
    """
    # 起點：當天 00:00:00
    start = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=tz)
    # 終點：當天 23:59:59
    end = datetime(date.year, date.month, date.day, 23, 59, 59, tzinfo=tz)

    # 轉回 UTC timestamp
    start_ts = int(start.astimezone(timezone.utc).timestamp())
    end_ts = int(end.astimezone(timezone.utc).timestamp())
    return start_ts, end_ts
