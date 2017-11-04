import logging
import sys

from mondrian import errors, filters, formatters, levels, term
from mondrian._version import __version__

__all__ = [
    '__version__',
    'errors',
    'filters',
    'formatters',
    'levels',
    'setup',
    'setup_excepthook',
    'term',
]


def setup_excepthook():
    """
    Replace default python exception hook with our own.

    """
    sys.excepthook = errors.excepthook


is_setup = False


def setup(*, colors=(not term.iswindows), excepthook=False):
    """
    Setup mondrian log handlers.

    :param colors: bool
    :param excepthook: bool
    """
    global is_setup

    if not is_setup:
        for level, name in levels.NAMES.items():
            logging.addLevelName(level, name)

        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(formatters.Formatter())
        handler.addFilter(filters.ColorFilter() if colors else filters.Filter())

        logging.getLogger().addHandler(handler)
        logging.captureWarnings(True)

        is_setup = True

    if excepthook:
        setup_excepthook()


def getLogger(*args, colors=(not term.iswindows), excepthook=False, **kwargs):
    setup(colors=colors, excepthook=excepthook)
    return logging.getLogger(*args, **kwargs)
