"""
Functions to parse datetime objects.

We're using regular expressions rather than time.strptime because:
- They provide both validation and parsing.
- They're more flexible for datetimes.
- The date/datetime/time constructors produce friendlier error messages.

Stolen from https://raw.githubusercontent.com/django/django/main/django/utils/dateparse.py at
9718fa2e8abe430c3526a9278dd976443d4ae3c6

Changed to:
* use standard python datetime types not django.utils.timezone
* raise ValueError when regex doesn't match rather than returning None
* support parsing unix timestamps for dates and datetimes
"""
import re
from datetime import date, datetime, time, timedelta, timezone
from typing import Dict, Optional, Type, Union
from pydantic.v1 import errors
date_expr = '(?P<year>\\d{4})-(?P<month>\\d{1,2})-(?P<day>\\d{1,2})'
time_expr = '(?P<hour>\\d{1,2}):(?P<minute>\\d{1,2})(?::(?P<second>\\d{1,2})(?:\\.(?P<microsecond>\\d{1,6})\\d{0,6})?)?(?P<tzinfo>Z|[+-]\\d{2}(?::?\\d{2})?)?$'
date_re = re.compile(f'{date_expr}$')
time_re = re.compile(time_expr)
datetime_re = re.compile(f'{date_expr}[T ]{time_expr}')
standard_duration_re = re.compile('^(?:(?P<days>-?\\d+) (days?, )?)?((?:(?P<hours>-?\\d+):)(?=\\d+:\\d+))?(?:(?P<minutes>-?\\d+):)?(?P<seconds>-?\\d+)(?:\\.(?P<microseconds>\\d{1,6})\\d{0,6})?$')
iso8601_duration_re = re.compile('^(?P<sign>[-+]?)P(?:(?P<days>\\d+(.\\d+)?)D)?(?:T(?:(?P<hours>\\d+(.\\d+)?)H)?(?:(?P<minutes>\\d+(.\\d+)?)M)?(?:(?P<seconds>\\d+(.\\d+)?)S)?)?$')
EPOCH = datetime(1970, 1, 1)
MS_WATERSHED = int(20000000000.0)
MAX_NUMBER = int(3e+20)
StrBytesIntFloat = Union[str, bytes, int, float]

def parse_date(value: Union[date, StrBytesIntFloat]) -> date:
    """
    Parse a date/int/float/string and return a datetime.date.

    Raise ValueError if the input is well formatted but not a valid date.
    Raise ValueError if the input isn't well formatted.
    """
    pass

def parse_time(value: Union[time, StrBytesIntFloat]) -> time:
    """
    Parse a time/string and return a datetime.time.

    Raise ValueError if the input is well formatted but not a valid time.
    Raise ValueError if the input isn't well formatted, in particular if it contains an offset.
    """
    pass

def parse_datetime(value: Union[datetime, StrBytesIntFloat]) -> datetime:
    """
    Parse a datetime/int/float/string and return a datetime.datetime.

    This function supports time zone offsets. When the input contains one,
    the output uses a timezone with a fixed offset from UTC.

    Raise ValueError if the input is well formatted but not a valid datetime.
    Raise ValueError if the input isn't well formatted.
    """
    pass

def parse_duration(value: StrBytesIntFloat) -> timedelta:
    """
    Parse a duration int/float/string and return a datetime.timedelta.

    The preferred format for durations in Django is '%d %H:%M:%S.%f'.

    Also supports ISO 8601 representation.
    """
    pass