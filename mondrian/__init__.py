import logging
from textwrap import indent
from traceback import format_exception

from colorama import Fore, Style

from mondrian._version import __version__
from mondrian.constants import CLEAR_EOL, iswindows

__all__ = [
    '__version__',
    'setup',
    'getLogger',
]

_setup = False
_setupExceptHook = False


def setup():
    global _setup
    if not _setup:
        _setup = True

        import sys
        from mondrian.filters import Filter
        from mondrian.formatters import Formatter
        logging.getLogger()

        def get_format():
            yield '{b}[%(fg)s%(levelname)s{b}][{w}'
            yield '{b}][{w}'.join(('%(spent)04d', '%(name)s'))
            yield '{b}]'
            yield ' %(fg)s%(message)s{r}'
            if not iswindows:
                yield CLEAR_EOL

        colors = {
            'b': '' if iswindows else Fore.LIGHTBLACK_EX,
            'w': '' if iswindows else Fore.LIGHTBLACK_EX,
            'r': '' if iswindows else Style.RESET_ALL,
        }
        format = (''.join(get_format())).format(**colors)
        logging.addLevelName(logging.DEBUG, 'DEBG')
        logging.addLevelName(logging.INFO, 'INFO')
        logging.addLevelName(logging.WARNING, 'WARN')
        logging.addLevelName(logging.ERROR, 'ERR ')
        logging.addLevelName(logging.CRITICAL, 'CRIT')
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(Formatter(format))
        handler.addFilter(Filter())
        logging.getLogger().addHandler(handler)

        logging.captureWarnings(True)


def _get_error_message(exc):
    if hasattr(exc, '__str__'):
        message = str(exc)
        return message[0].upper() + message[1:]
    return '\n'.join(exc.args),


def excepthook(exctype, exc, traceback, level=logging.CRITICAL, logger=None, context=None):
    """
    Error handler. Whatever happens in a plugin or component, if it looks like an exception, taste like an exception
    or somehow make me think it is an exception, I'll handle it.

    :param exc: the culprit
    :param trace: Hercule Poirot's logbook.
    :return: to hell
    """
    logger = logger or logging.getLogger()
    formatted_exception = format_exception(exctype, exc, traceback)

    EOL = Style.RESET_ALL + CLEAR_EOL + '\n'
    prefix = '{} \u2502 {}'.format(Fore.RED, Style.RESET_ALL)

    logger.log(
        level,
        EOL.join(
            [
                Fore.RED + (str(context) if context else formatted_exception[0].strip()),
                *(indent(frame.strip(), prefix) for frame in formatted_exception[1:-1]),
                prefix + Fore.RED + exctype.__name__ + ': ' + Fore.WHITE + str(exc)
            ]
        )
    )


def setupExceptHook():
    global _setupExceptHook
    if not _setupExceptHook:
        import sys
        sys.excepthook = excepthook


def getLogger(name=None):
    setup()
    return logging.getLogger(name)
