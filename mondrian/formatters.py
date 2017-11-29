import logging
import re
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

        output = []
        stack_length = len(formatted_exception)
        for i, frame in enumerate(formatted_exception):
            if frame.startswith('  '):
                output.append(textwrap.indent('  ' + frame.strip(), lightblack('\u2502 ')))
            else:
                g = re.match('([a-zA-Z.]+): (.*)$', frame.strip(), flags=re.DOTALL)
                if g is not None:
                    etyp, emsg = g.group(1), g.group(2)
                    output.append(
                        lightblack('\u2514' if i + 1 == stack_length else '\u251c') +
                        lightblack_bg(lightwhite(' ' + etyp + ' ')) + ' ' +
                        lightwhite(textwrap.indent(str(emsg), ' ' * (len(etyp) + 4)).strip())
                    )
                else:
                    output.append(textwrap.indent(frame.strip(), lightblack('\u2502 ')))

        return EOL.join(output)
