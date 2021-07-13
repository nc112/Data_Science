#! python project
# -*- coding:utf8 -*-
# -------------------------
#    Filename: common_func.py
#      Author: Nicolas
# Create date: 2021-06-22
# Description:
# logging function
# --------------------------
import logging
from os import path
from os import makedirs
from platform import system

'''
logging level:
_levelToName = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
    NOTSET: 'NOTSET',
}

_nameToLevel = {
    'CRITICAL': CRITICAL,
    'FATAL': FATAL,
    'ERROR': ERROR,
    'WARN': WARNING,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}
'''

class Logger:
    def __init__(self, loggername, logger_path, log_level='DEBUG'):
        # Init a logger
        # TODO: set level, update later
        log_level = logging.DEBUG

        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(log_level)

        # Create a handler for write logs
        log_path = logger_path + '/logs/'
        if not path.exists(log_path):
            makedirs(log_path)

        logname = log_path + 'reminder.log'

        # for debug only
        #print(log_path)

        logger_fh = logging.FileHandler(logname, encoding='utf-8')
        logger_fh.setLevel(log_level)

        # Create a handler for show logs to console
        logger_ch = logging.StreamHandler()
        logger_ch.setLevel(log_level)

        # Create a logging, TODO: optimize the logging format later
        formatter = logging.Formatter('%(asctime)s [%(name)s] <%(levelname)s>  %(message)s')
        logger_fh.setFormatter(formatter)
        logger_ch.setFormatter(formatter)

        self.logger.addHandler(logger_fh)
        self.logger.addHandler(logger_ch)

    def get_log(self):
        #TODO: update: can overwrite here
        return self.logger