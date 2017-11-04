import logging
import textwrap
from traceback import format_exception

from colorama import Style

from mondrian.term import iswindows, lightblack, CLEAR_EOL, lightblack_bg, lightwhite

EOL = '\n' if iswindows else (Style.RESET_ALL + CLEAR_EOL + '\n')


class _Style(logging.PercentStyle):
    def __init__(self):
        tokens = (
            '%(color)s%(levelname)s',
            '%(spent)04d',
            '%(name)s',
        )

        sep = '|' if iswindows else (Style.RESET_ALL + lightblack(':'))
        self._fmt = sep.join(tokens) + lightblack(':') + ' %(message)s' + EOL.strip()


class Formatter(logging.Formatter):
    def __init__(self):
        self._style = _Style()
        self._fmt = self._style._fmt

    def formatException(self, excinfo):
        formatted_exception = format_exception(*excinfo)

        return EOL.join(
            [
                *(textwrap.indent(frame.strip(), lightblack('\u2502 ')) for frame in formatted_exception[:-1]),
                lightblack('\u2514') + lightblack_bg(lightwhite(' ' + excinfo[0].__name__ + ' ')) + ' ' +
                lightwhite(textwrap.indent(str(excinfo[1]), ' ' * (len(excinfo[0].__name__) + 4)).strip())
            ]
        )
