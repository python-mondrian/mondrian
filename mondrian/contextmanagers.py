import re
import sys
from contextlib import contextmanager
from sys import exc_info

from mondrian import settings, term
from mondrian.formatters import format_exception
from mondrian.styles import BOTTOM_LEFT, BOTTOM_RIGHT, HORIZ, TOP_LEFT, TOP_RIGHT, VERT, VERT_LEFT

reaesc = re.compile(r"\x1b[^m]*m")


@contextmanager
def humanize(*, types=(Exception,)):
    if not isinstance(types, tuple):
        types = (types,)

    try:
        yield
    except types as exc:
        SPACES = 2
        fg = term.red
        bg = lambda *args: term.red_bg(term.bold(*args))
        prefix = fg(VERT + " " * (SPACES - 1))
        suffix = fg(" " * (SPACES - 1) + VERT)

        pre_re = re.compile("([^`]*)`([^`]*)`([^`]*)")

        def format_arg(arg):
            length = len(pre_re.sub("\\1\\2\\3", arg))

            arg = pre_re.sub("\\1" + term.bold("\\2") + "\\3", arg)
            arg = re.sub("^  \$ (.*)", term.lightblack("  $ ") + term.reset("\\1"), arg)

            return (arg, length)

        def f(*args):
            return "".join(args)

        term_width, term_height = term.get_size()
        line_length = min(80, term_width)
        for arg in exc.args:
            line_length = max(min(line_length, len(arg) + 2 * SPACES), 120)

        print(f(fg(TOP_LEFT + HORIZ * (line_length - 2) + TOP_RIGHT)), file=sys.stderr)

        for i, arg in enumerate(exc.args):

            if i == 1:
                print(f(prefix, " " * (line_length - 2 * SPACES), suffix), file=sys.stderr)

            arg_formatted, arg_length = format_arg(arg)
            if not i:
                # first line
                print(
                    f(
                        prefix,
                        bg(" " + type(exc).__name__ + " "),
                        " ",
                        term.white(arg_formatted),
                        " " * (line_length - (arg_length + 3 + len(type(exc).__name__) + 2 * SPACES)),
                        suffix,
                    ),
                    file=sys.stderr,
                )
            else:
                # other lines
                print(f(prefix, arg_formatted + " " * (line_length - arg_length - 2 * SPACES), suffix), file=sys.stderr)

        print(
            f(fg((VERT_LEFT if settings.DEBUG else BOTTOM_LEFT) + HORIZ * (line_length - 2) + BOTTOM_RIGHT)),
            file=sys.stderr,
        )

        if settings.DEBUG:
            # print(, file=sys.stderr)
            for _line in format_exception(exc_info(), fg=fg, bg=bg, summary=False).splitlines():
                print(_line, file=sys.stderr)

            print(f(fg("╵")), file=sys.stderr)
