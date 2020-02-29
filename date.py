import sys
import os
import datetime as dt
import calendar


if sys.version_info[0] < 3:
    raise RuntimeError("Oh, so you're one of THOSE people.")
if sys.version_info[1] < 8:
    raise RuntimeError('Upgrade to Python 3.8 for walruses.')


class Date:

    date_format = '%Y-%m-%d'

    def __init__(self, *args, **kwargs):
        if args and isinstance(string := args[0], str):
            self.datetime = dt.datetime.strptime(string, self.date_format)
        elif 'string' in kwargs and (string := kwargs['string']):
            self.datetime = dt.datetime.strptime(string, self.date_format)
        elif args and isinstance(datetime := args[0], dt.datetime):
            self.datetime = Date.set_to_midnight(datetime)
        elif 'datetime' in kwargs and (datetime := kwargs['datetime']):
            self.datetime = Date.set_to_midnight(datetime)
        elif args and len(args) == 3:
            self.datetime = dt.datetime(int(args[0]), int(args[1]), int(args[2]))
        elif {'year', 'month', 'day'}.issubset(kwargs):
            self.datetime = dt.datetime(int(kwargs['year']),
                                        int(kwargs['month']),
                                        int(kwargs['day']))
        else:
            raise RuntimeError('Improper initialization of Date class.')

    def __str__(self):
        return self.datetime.strftime(self.date_format)

    def __repr__(self):
        return f'{self.datetime.month}/{self.datetime.day}/{self.datetime.year}'
        
    @classmethod
    def today(cls):
        today = dt.datetime.today()
        return Date(today.year, today.month, today.day)

    @classmethod
    def set_to_midnight(cls, datetime):
        return dt.datetime(datetime.year, datetime.month, datetime.day)

    def __sub__(self, *args, **kwargs):
        if args and isinstance(num_days := args[0], int):
            return Date(self.datetime - dt.timedelta(days=num_days))
        elif args and isinstance(timedelta := args[0], dt.timedelta):
            return Date(self.datetime - timedelta)
        elif args and isinstance(date := args[0], Date):
            return (self.datetime - date.datetime).days
        elif 'num_days' in kwargs and (num_days := kwargs['num_days']):
            return Date(self.datetime - dt.timedelta(days=num_days))
        elif 'timedelta' in kwargs and (timedelta := kwargs['timedelta']):
            return Date(self.datetime - timedelta)
        elif 'date' in kwargs and (date := kwargs['date']):
            return (self.datetime - date.datetime).days

    def __add__(self, *args, **kwargs):
        if args and isinstance(num_days := args[0], int):
            return Date(self.datetime + dt.timedelta(days=num_days))
        elif args and isinstance(timedelta := args[0], dt.timedelta):
            return Date(self.datetime + timedelta)
        elif 'num_days' in kwargs and (num_days := kwargs['num_days']):
            return Date(self.datetime + dt.timedelta(days=num_days))
        elif 'timedelta' in kwargs and (timedelta := kwargs['timedelta']):
            return Date(self.datetime + timedelta)

    @property
    def is_weekday(self):
        return calendar.weekday(self.datetime.year,
                                self.datetime.month,
                                self.datetime.day) <= 4

    @property
    def year(self):
        return self.datetime.year

    @property
    def month(self):
        return self.datetime.month

    @property
    def day(self):
        return self.datetime.day

    def nextmonth(self):
        return calendar._nextmonth(self.year, self.month)

    def prevmonth(self):
        return calendar._prevmonth(self.year, self.month)

    def endmonth_payday(self):
        day = calendar.monthrange(self.year, self.month)[1]
        payday = Date(self.year, self.month, day)
        while not payday.is_weekday:
            payday -= 1
        return payday

    def midmonth_payday(self):
        day = 15
        payday = Date(self.year, self.month, day)
        while not payday.is_weekday:
            payday -= 1
        return payday

    def __eq__(self, date):
        return self.datetime == Date.set_to_midnight(date)

    def __le__(self, date):
        return self.datetime <= Date.set_to_midnight(date)

    def __lt__(self, date):
        return self.datetime <= Date.set_to_midnight(date)

    def __ge__(self, date):
        return self.datetime >= Date.set_to_midnight(date)

    def __gt__(self, date):
        return self.datetime > Date.set_to_midnight(date)

    def __ne__(self, date):
        return self.datetime != Date.set_to_midnight(date)

    @classmethod
    def first_of_month(self):
        today = Date.today()
        return Date(today.year, today.month, 1)

    @classmethod
    def last_of_month(self):
        today = Date.today()
        num_days = calendar.monthrange(today.year, today.month)[1]
        return Date(today.year, today.month, num_days)

    def paydays(self):
        today = Date.today()
        this_midmonth_payday = today.midmonth_payday()
        this_endmonth_payday = today.endmonth_payday()
        prev_midmonth_payday = (Date.first_of_month() - 1).midmonth_payday()
        prev_endmonth_payday = (Date.first_of_month() - 1).endmonth_payday()
        next_midmonth_payday = (Date.last_of_month() + 1).midmonth_payday()
        if this_endmonth_payday <= self <= Date.last_of_month():
            return this_midmonth_payday, this_endmonth_payday, next_midmonth_payday
        elif this_midmonth_payday <= self < this_endmonth_payday:
            return prev_endmonth_payday, this_midmonth_payday, this_endmonth_payday
        else:
            return prev_midmonth_payday, prev_endmonth_payday, this_midmonth_payday

    def prev_payday(self):
        return self.paydays()[0]

    def payday(self):
        return self.paydays()[1]

    def next_payday(self):
        return self.paydays()[2]
        
