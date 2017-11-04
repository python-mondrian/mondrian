import logging

from colorama import Fore

from mondrian import levels


class Filter(logging.Filter):
    def filter(self, record):
        record.color = ''
        record.spent = record.relativeCreated // 1000
        return True


class ColorFilter(Filter):
    def filter(self, record):
        super().filter(record)
        record.color = levels.COLORS.get(record.levelname, Fore.LIGHTWHITE_EX)
        return True
