__config__ = 'sportech-helper-logging.yml'

from bookie import config as configuration

config = configuration.data('sportech.helper.logging')

# internal imports should go after configuration not to get recursion
from sportech.helper.logging.logger import get_logger  # noqa: E402
from sportech.helper.logging.adapter import BOTLoggerAdapter  # noqa: E402
from sportech.helper.logging.formatter import BOTLogFormatter  # noqa: E402

__all__ = [
    '__config__',
    'config',
    'get_logger',
    'BOTLoggerAdapter',
    'BOTLogFormatter',
]
