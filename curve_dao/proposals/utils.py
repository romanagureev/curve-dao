import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"


def get_datestring(ts):
    dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
    return dt.strftime(TIME_FORMAT)
