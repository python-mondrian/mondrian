import logging

from colorama import Fore

DEBUG = 'DEBG'
INFO = 'INFO'
WARNING = 'WARN'
ERROR = 'ERR.'
CRITICAL = 'CRIT'

COLORS = {
    DEBUG: Fore.LIGHTCYAN_EX,
    INFO: Fore.LIGHTWHITE_EX,
    WARNING: Fore.LIGHTYELLOW_EX,
    ERROR: Fore.LIGHTRED_EX,
    CRITICAL: Fore.RED,
}

NAMES = {
    logging.DEBUG: DEBUG,
    logging.INFO: INFO,
    logging.WARNING: WARNING,
    logging.ERROR: ERROR,
    logging.CRITICAL: CRITICAL,
}
