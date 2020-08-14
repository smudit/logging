# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from collections import OrderedDict
from datetime import date, datetime
from json import dumps

from pythonjsonlogger.jsonlogger import JsonFormatter


class BOTLogFormatter(JsonFormatter):
    def format(self, record):
        msg = OrderedDict()
        msg['asctime'] = datetime.utcnow().isoformat()
        msg['name'] = record.name
        msg['levelname'] = record.levelname
        msg['func'] = record.funcName
        if isinstance(record.msg, dict):
            for k, v in record.msg.items():
                # Limit float values to 4 decimal places for logging
                if type(v) is float:
                    record.msg[k] = '{:.4f}'.format(v)
                if isinstance(v, date):
                    record.msg[k] = v.isoformat()
        msg.update(record.msg)

        return dumps(msg)
