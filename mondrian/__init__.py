from logging import addLevelName, DEBUG, INFO, WARNING, ERROR, CRITICAL, StreamHandler, getLogger as _getLogger

from colorama import Fore, Style

from mondrian._version import __version__
from mondrian.constants import CLEAR_EOL, iswindows

_root_logger = None


def getLogger():
    global _root_logger
    if _root_logger is None:
        import sys
        from mondrian.filters import Filter
        from mondrian.formatters import Formatter

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

        addLevelName(DEBUG, 'DEBG')
        addLevelName(INFO, 'INFO')
        addLevelName(WARNING, 'WARN')
        addLevelName(ERROR, 'ERR ')
        addLevelName(CRITICAL, 'CRIT')
        handler = StreamHandler(sys.stderr)
        handler.setFormatter(Formatter(format))
        handler.addFilter(Filter())
        _root_logger = _getLogger()
        _root_logger.addHandler(handler)
    return _root_logger
