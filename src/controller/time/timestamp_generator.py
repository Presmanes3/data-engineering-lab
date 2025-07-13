import datetime

import pandas as pd


class TimestampGenerator:

    @classmethod
    def generate_timestamps(
        cls,
        start_hour: int = 0,
        end_hour: int = 23,
        interval_seconds: int = 19,
        date: datetime.date | None = None
    ) -> 'Generator[datetime.datetime, None, None]':
        if date is None:
            date = datetime.datetime.now().date()

        start: datetime.datetime = datetime.datetime.combine(date, datetime.time.min) + datetime.timedelta(hours=start_hour)
        end: datetime.datetime = datetime.datetime.combine(date, datetime.time.min) + datetime.timedelta(hours=end_hour)

        current: datetime.datetime = start
        while current <= end:
            yield current
            current += datetime.timedelta(seconds=interval_seconds)

    @classmethod
    def get_timestamp_vector(
        cls,
        start_hour: int = 0,
        end_hour: int = 23,
        interval_seconds: int = 19,
        date: datetime.date | None = None
    ) -> list[datetime.datetime]:
        return list(cls.generate_timestamps(start_hour, end_hour, interval_seconds, date))
    
    @classmethod
    def get_timestamp_series(
        cls,
        start_hour: int = 0,
        end_hour: int = 23,
        interval_seconds: int = 19,
        date: datetime.date | None = None
    ) -> pd.DatetimeIndex:
        if date is None:
            date = datetime.datetime.now().date()

        start = datetime.datetime.combine(date, datetime.time.min) + datetime.timedelta(hours=start_hour)
        end = datetime.datetime.combine(date, datetime.time.min) + datetime.timedelta(hours=end_hour)

        return pd.date_range(start=start, end=end, freq=f"{interval_seconds}s")
    

if __name__ == "__main__":
    # Example usage
    # timestamps = TimestampGenerator.get_timestamp_vector(start_hour=0, end_hour=1, interval_seconds=10)
    # for ts in timestamps:
    #     print(ts)
    
    timestamp_series = TimestampGenerator.get_timestamp_series(start_hour=8, end_hour=12, interval_seconds=60)
    print(timestamp_series)