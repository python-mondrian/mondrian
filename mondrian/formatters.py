import logging
import re
import textwrap
from traceback import format_exception as _format_exception

from colorama import Style

from mondrian import settings, styles
from mondrian.term import CLEAR_EOL, iswindows, lightblack, lightblack_bg, lightwhite

if iswindows or not settings.COLORS:
    EOL = "\n"
else:
    EOL = Style.RESET_ALL + CLEAR_EOL + "\n"


class _Style(logging.PercentStyle):
    def __init__(self):
        tokens = ("%(color)s%(levelname)s", "%(spent)04d", "%(name)s")

        sep = "|" if iswindows else (Style.RESET_ALL + lightblack(":"))
        self._fmt = sep.join(tokens) + lightblack(":") + " %(message)s" + EOL.strip()


def format_exception(excinfo, *, prefix="", fg=lightblack, bg=lightblack_bg, summary=True):
    formatted_exception = _format_exception(*excinfo)

    output = []
    stack_length = len(formatted_exception)
    for i, frame in enumerate(formatted_exception):
        _last = i + 1 == stack_length
        if frame.startswith("  "):
            output.append(textwrap.indent("  " + frame.strip(), fg("\u2502 ")))
        else:
            # XXX TODO change this to use valid python package regexp (plus dot).
            g = re.match("([a-zA-Z_.]+): (.*)$", frame.strip(), flags=re.DOTALL)
            if summary or not _last:
                if g is not None:
                    etyp, emsg = g.group(1), g.group(2)
                    output.append(
                        fg(styles.BOTTOM_LEFT if _last else styles.VERT_LEFT)
                        + bg(lightwhite(" " + etyp + " "))
                        + " "
                        + lightwhite(textwrap.indent(str(emsg), " " * (len(etyp) + 4)).strip())
                    )
                else:
                    output.append(textwrap.indent(frame.strip(), fg("\u2502 ")))

    return textwrap.indent(EOL.join(output), prefix=prefix)


class Formatter(logging.Formatter):
    def __init__(self):
        self._style = _Style()
        self._fmt = self._style._fmt

    formatException = staticmethod(format_exception)
