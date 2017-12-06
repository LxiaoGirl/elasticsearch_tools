#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: xiaoL-pkav l@pker.in
@version: 2017/12/06 16:29
"""


from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler
import logging.handlers
import sys

FORMATTER = logging.Formatter('\r%(asctime)s [%(name)s][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
FORMATTER_FILE = logging.Formatter('%(asctime)s [%(name)s][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
COLOR_LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
COLOR_LOGGER_HANDLER.setFormatter(FORMATTER)

time_file_handler = logging.handlers.TimedRotatingFileHandler('./logs/logs', 'S', 1)
time_file_handler.setFormatter(FORMATTER_FILE)
time_file_handler.suffix = "%Y-%m-%d.log"
time_file_handler.setLevel(logging.INFO)

class MyLogger(logging.getLoggerClass()):
    def __init__(self, name):
        super(MyLogger, self).__init__(self)
        self.name = name
        self.addHandler(COLOR_LOGGER_HANDLER)
        self.addHandler(time_file_handler)

Logger = MyLogger("ES_TO_FILE")
