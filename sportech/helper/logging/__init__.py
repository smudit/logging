__config__ = 'sportech-helper-logging.yml'



# internal imports should go after configuration not to get recursion
from sportech.helper.logging.logger import get_logger  # noqa: E402
from sportech.helper.logging.adapter import BOTLoggerAdapter  # noqa: E402
from sportech.helper.logging.formatter import BOTLogFormatter  # noqa: E402

__all__ = [
    '__config__',
    'get_logger',
    'BOTLoggerAdapter',
    'BOTLogFormatter',
]
