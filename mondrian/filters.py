import logging

from colorama import Fore

from mondrian import iswindows


class Filter(logging.Filter):
    def filter(self, record):
        record.spent = record.relativeCreated // 1000
        if iswindows:
            record.fg = ''
        elif record.levelname == 'DEBG':
            record.fg = Fore.LIGHTBLACK_EX
        elif record.levelname == 'INFO':
            record.fg = Fore.LIGHTWHITE_EX
        elif record.levelname == 'WARN':
            record.fg = Fore.LIGHTYELLOW_EX
        elif record.levelname == 'ERR ':
            record.fg = Fore.LIGHTRED_EX
        elif record.levelname == 'CRIT':
            record.fg = Fore.RED
        else:
            record.fg = Fore.LIGHTWHITE_EX
        return True