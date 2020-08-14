# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import logging
import sys
import traceback

import jsonpickle


class BOTLoggerAdapter(logging.LoggerAdapter):

    def __init__(self, log, extra, **kwargs):
        super(BOTLoggerAdapter, self).__init__(log, extra=extra)
        self.endpoint = kwargs.get('endpoint', None)

    def process(self, msg, kwargs):
        msg, kwargs = super(BOTLoggerAdapter, self).process(msg, kwargs)
        if not isinstance(msg, dict):
            msg = dict(message=msg)
        if self.endpoint:
            msg.update({'endpoint': self.endpoint})

        return msg, kwargs

    def race_error(self, race_id, message):
        msg = {
            'race_id': race_id,
            'message': message,
        }
        if isinstance(message, dict):
            message.update(msg)
        self.log(logging.ERROR, msg)

    def bet(self, betting_pool, race_id, message):
        msg = {
            'betting_pool': betting_pool,
            'race_id': race_id,
        }
        if isinstance(message, dict):
            message.update(msg)
        self.log(logging.INFO, message)

    def exception(self, msg, *args, **kwargs):
        self.log(logging.ERROR, {
            'message': '%s (%s)' % (msg, str(sys.exc_info()[1])),
            'traceback': str(jsonpickle.encode(traceback.format_exc())),
        })
