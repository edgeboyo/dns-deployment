from datetime import datetime, timedelta
from datetime import datetime

isoFormat = '%Y-%m-%dT%H:%M:%S.%fZ'

epoch = datetime(1970, 1, 1)


def stampToISO(ts):
    actualTime = epoch + timedelta(seconds=ts)
    return actualTime.strftime(isoFormat)


def ISOToStamp(isoTime):
    ts = (datetime.strptime(isoTime, isoFormat) - epoch).total_seconds()
    return ts
