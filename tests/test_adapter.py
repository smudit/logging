# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import logging
import sys
import traceback

import jsonpickle
import pytest

from sportech.helper.logging import BOTLoggerAdapter


@pytest.fixture
def adapter(mocker):
    logger = mocker.Mock(name='logger')
    return BOTLoggerAdapter(log=logger, extra={}, endpoint=None)


@pytest.mark.parametrize('message,endpoint,result', [
    (dict(key='dummy'), 'https://google.com', dict(key='dummy', endpoint='https://google.com')),
    (dict(key='dummy'), None, dict(key='dummy')),
    ('dummy', 'https://google.com', dict(message='dummy', endpoint='https://google.com')),
    ('dummy', None, dict(message='dummy')),
])
def test_process(mocker, message, endpoint, result):
    super_process_mock = mocker.patch.object(logging.LoggerAdapter, 'process')
    super_process_mock.return_value = message, dict()
    logger = mocker.Mock(name='logger')
    adapter = BOTLoggerAdapter(log=logger, extra={}, endpoint=endpoint)

    assert (result, dict()) == adapter.process(message, kwargs=dict())


def test_race_error_with_non_dict_message(mocker, adapter):
    log_mock = mocker.patch.object(BOTLoggerAdapter, 'log')
    race_id = mocker.Mock(name='race_id')
    message = mocker.Mock(name='message')

    adapter.race_error(race_id=race_id, message=message)

    log_mock.assert_called_once_with(logging.ERROR, dict(
        race_id=race_id,
        message=message,
    ))


def test_race_error_with_dict_message(mocker, adapter):
    log_mock = mocker.patch.object(BOTLoggerAdapter, 'log')
    race_id = mocker.Mock(name='race_id')
    message = dict(existing_key='existing_value')

    adapter.race_error(race_id=race_id, message=message)

    log_mock.assert_called_once_with(logging.ERROR, dict(
        race_id=race_id,
        message=message,
    ))


def test_bet_with_non_dict_message(mocker, adapter):
    log_mock = mocker.patch.object(BOTLoggerAdapter, 'log')
    betting_pool = mocker.Mock(name='betting_pool')
    race_id = mocker.Mock(name='race_id')
    message = mocker.Mock(name='message')

    adapter.bet(betting_pool=betting_pool, race_id=race_id, message=message)

    log_mock.assert_called_once_with(logging.INFO, message)


def test_bet_with_dict_message(mocker, adapter):
    log_mock = mocker.patch.object(BOTLoggerAdapter, 'log')
    betting_pool = mocker.Mock(name='betting_pool')
    race_id = mocker.Mock(name='race_id')
    message = dict(existing_key='existing_value')

    adapter.bet(betting_pool=betting_pool, race_id=race_id, message=message)

    log_mock.assert_called_once_with(logging.INFO, dict(
        betting_pool=betting_pool,
        race_id=race_id,
        existing_key='existing_value',
    ))


def test_exception(mocker, adapter):
    msg_mock = mocker.Mock(name='msg')
    log_mock = mocker.patch.object(BOTLoggerAdapter, 'log')
    try:
        1/0
    except ZeroDivisionError:
        exc_info = sys.exc_info()
        formatted_exc = traceback.format_exc()
        adapter.exception(msg_mock)

        log_mock.assert_called_once_with(
            logging.ERROR, {
                'message': '%s (%s)' % (msg_mock, str(exc_info[1])),
                'traceback': str(jsonpickle.encode(formatted_exc)),
            }
        )
    else:
        assert False, 'exception should be raised'
