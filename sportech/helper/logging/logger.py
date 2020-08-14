# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import logging
import logging.handlers
import os

from typing import Text, Optional  # noqa: F401

from sportech.helper.logging.adapter import BOTLoggerAdapter
from sportech.helper.logging.formatter import BOTLogFormatter


def _get_default_logger(name):
    return logging.getLogger(name)


def get_logger(name, log_dir, level=logging.INFO, endpoint=None, max_bytes=50 * 1024 * 1024, backup_count=20):
    # type: (Text, Text, int, Optional[Text], Optional[int], Optional[int]) -> 'BOTLoggerAdapter'
    log = _get_default_logger(name)
    file_path = os.path.join(log_dir, name)
    if not file_path.endswith('log'):
        file_path += '.log'
    handler = logging.handlers.RotatingFileHandler(filename=file_path, maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(BOTLogFormatter())
    log.addHandler(handler)
    log.setLevel(level)
    log_adapter = BOTLoggerAdapter(log=log, extra={}, endpoint=endpoint)
    return log_adapter
