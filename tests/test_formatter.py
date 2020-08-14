# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import json
import logging
from collections import OrderedDict
from datetime import date, datetime
from uuid import uuid4

import pytest

from sportech.helper.logging import BOTLogFormatter


@pytest.fixture()
def log_record():
    return logging.LogRecord(
        name='d8c00b0e84fc4d9da4f639d6a1a8810c',
        level=logging.INFO,
        pathname='/test.py',
        lineno=20,
        msg={
            'int': 1,
            'float1': 1.0,
            'float2': 0.6666666,
            'date': date(2018, 12, 31),
            'datetime': datetime(2018, 8, 31, 14),
        },
        args=(),
        exc_info=None,
    )


@pytest.mark.freeze_time('2018-08-28')
def test_format(log_record):
    json_serialized = BOTLogFormatter().format(log_record)
    json_deserialized = json.loads(json_serialized)

    assert {
        'asctime': '2018-08-28T00:00:00',
        'name': 'd8c00b0e84fc4d9da4f639d6a1a8810c',
        'levelname': 'INFO',
        'func': None,
        'int': 1,
        'float1': '1.0000',
        'float2': '0.6667',
        'date': '2018-12-31',
        'datetime': '2018-08-31T14:00:00',
    } == json_deserialized
