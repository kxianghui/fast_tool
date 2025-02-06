# -*- coding: utf-8 -*-
__author__ = 'hkhl'


import datetime


def format_time(time, pattern='%Y-%m-%d %H:%M:%S'):
    return time.strftime(pattern)


def format_now(pattern='%Y-%m-%d %H:%M:%S'):
    return format_time(datetime.datetime.now(), pattern)