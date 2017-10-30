import logging
import textwrap

from colorama import Fore

from mondrian import iswindows


class Formatter(logging.Formatter):
    def formatException(self, ei):
        tb = super().formatException(ei)
        if iswindows:
            return textwrap.indent(tb, ' | ')
        else:
            return textwrap.indent(tb, Fore.BLACK + ' | ' + Fore.WHITE)