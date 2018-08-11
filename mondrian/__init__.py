import codecs
import logging
import sys

from mondrian import errors, filters, formatters, levels, term
from mondrian._version import __version__

__all__ = ["__version__", "errors", "filters", "formatters", "levels", "setup", "setup_excepthook", "term"]

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


def setup(*, colors=term.usecolors, excepthook=False, formatter=None):
    """
    Setup mondrian log handlers.

    :param colors: bool
    :param excepthook: bool
    """
    global is_setup

    if not is_setup:
        handler = logging.StreamHandler(sys.stderr)

        if formatter:
            handler.setFormatter(formatter)
        else:
            for level, name in levels.NAMES.items():
                logging.addLevelName(level, name)
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
