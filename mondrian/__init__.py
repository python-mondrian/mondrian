import codecs
import logging
import sys

from mondrian import errors, filters, formatters, humanizer, levels, settings, term
from mondrian._version import __version__

__all__ = [
    "__version__",
    "humanizer",
    "errors",
    "filters",
    "formatters",
    "levels",
    "settings",
    "setup",
    "setup_excepthook",
    "term",
]

# Patch standard output/error if it's not supporting unicode
# See: https://stackoverflow.com/questions/27347772/print-unicode-string-in-python-regardless-of-environment
if sys.stdout.encoding is None or sys.stdout.encoding == "ANSI_X3.4-1968":
    sys.stdout = codecs.getwriter("UTF-8")(sys.stdout.buffer, errors="replace")
    sys.stderr = codecs.getwriter("UTF-8")(sys.stderr.buffer, errors="replace")


def setup_excepthook():
    """
    Replace default python exception hook with our own.

    """
    sys.excepthook = errors.excepthook


is_setup = False


def setup(*, level=None, colors=term.usecolors, excepthook=False, formatter=None):
    """
    Setup mondrian log handlers.

    :param colors: bool
    :param excepthook: bool
    """
    global is_setup

    logger = logging.getLogger()

    if not is_setup:
        handler = logging.StreamHandler(sys.stderr)

        if formatter:
            handler.setFormatter(formatter)
        else:
            for _level, _name in levels.NAMES.items():
                logging.addLevelName(_level, _name)
            handler.setFormatter(formatters.Formatter())

        handler.addFilter(filters.ColorFilter() if colors else filters.Filter())
        logger.addHandler(handler)
        logging.captureWarnings(True)

        is_setup = True

    if excepthook:
        setup_excepthook()

    if level is None:
        # set default based on env
        logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    elif level is not False:
        logger.setLevel(level)


def getLogger(*args, colors=(not term.iswindows), excepthook=False, **kwargs):
    setup(colors=colors, excepthook=excepthook)
    return logging.getLogger(*args, **kwargs)
