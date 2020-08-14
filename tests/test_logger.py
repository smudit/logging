# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import logging
from logging.handlers import RotatingFileHandler

import six

from sportech.helper.logging import get_logger


def test_get_logger_integration(mocker, caplog):
    # prevent file creation
    mocker.patch.object(RotatingFileHandler, '_open')
    # prevent log emission
    mocker.patch.object(RotatingFileHandler, 'emit')

    log = get_logger('test_logger', '.')
    log.info('dummy message')

    assert len(caplog.record_tuples) == 1
    logger_name, logger_level, message = caplog.record_tuples[0]
    assert 'test_logger' == logger_name
    assert logging.INFO == logger_level
    assert six.text_type(dict(message='dummy message')) == message


def test_get_logger_unit(mocker):
    # params mocks
    logger_name_mock = 'test_logger'
    log_dir_mock = '.'
    level_mock = mocker.Mock(name='level')
    endpoint_mock = mocker.Mock(name='endpoint')
    max_bytes_mock = mocker.Mock(name='max_bytes')
    backup_count_mock = mocker.Mock(name='backup_count')

    logger_mock = mocker.Mock(name='logger')
    default_get_logger_mock = mocker.patch(get_logger.__module__ + '._get_default_logger')
    default_get_logger_mock.return_value = logger_mock
    handler_mock = mocker.Mock(name='handler')
    handler_cls_mock = mocker.patch(get_logger.__module__ + '.logging.handlers.RotatingFileHandler')
    handler_cls_mock.return_value = handler_mock
    adapter_mock = mocker.Mock(name='adapter')
    adapter_cls_mock = mocker.patch(get_logger.__module__ + '.BOTLoggerAdapter')
    adapter_cls_mock.return_value = adapter_mock
    formatter_mock = mocker.Mock(name='formatter')
    formatter_cls_mock = mocker.patch(get_logger.__module__ + '.BOTLogFormatter')
    formatter_cls_mock.return_value = formatter_mock

    adapter = get_logger(
        name=logger_name_mock,
        log_dir=log_dir_mock,
        level=level_mock,
        endpoint=endpoint_mock,
        max_bytes=max_bytes_mock,
        backup_count=backup_count_mock,
    )

    assert adapter is adapter_mock
    default_get_logger_mock.assert_called_once_with(logger_name_mock)
    handler_cls_mock.assert_called_once_with(
        filename='./test_logger.log', maxBytes=max_bytes_mock, backupCount=backup_count_mock)
    formatter_cls_mock.assert_called_once_with()
    handler_mock.setFormatter.assert_called_once_with(formatter_mock)
    logger_mock.addHandler.assert_called_once_with(handler_mock)
    logger_mock.setLevel.assert_called_once_with(level_mock)
    adapter_cls_mock.assert_called_once_with(log=logger_mock, extra={}, endpoint=endpoint_mock)
