import sys

from colorama import Fore, Back, Style

iswindows = (sys.platform == 'win32')
istty = sys.stdout.isatty()


def _create_color_wrappers(symbol):
    fg, bg = getattr(Fore, symbol), getattr(Back, symbol)

    def fg_wrapper(*args):
        return ''.join((fg, *args, Fore.RESET))

    def bg_wrapper(*args):
        return ''.join((bg, *args, Back.RESET))

    return fg_wrapper, bg_wrapper


black, black_bg = _create_color_wrappers('BLACK')
red, red_bg = _create_color_wrappers('RED')
green, green_bg = _create_color_wrappers('GREEN')
yellow, yellow_bg = _create_color_wrappers('YELLOW')
blue, blue_bg = _create_color_wrappers('BLUE')
magenta, magenta_bg = _create_color_wrappers('MAGENTA')
cyan, cyan_bg = _create_color_wrappers('CYAN')
white, white_bg = _create_color_wrappers('WHITE')
reset, reset_bg = _create_color_wrappers('RESET')
lightblack, lightblack_bg = _create_color_wrappers('LIGHTBLACK_EX')
lightred, lightred_bg = _create_color_wrappers('LIGHTRED_EX')
lightgreen, lightgreen_bg = _create_color_wrappers('LIGHTGREEN_EX')
lightyellow, lightyellow_bg = _create_color_wrappers('LIGHTYELLOW_EX')
lightblue, lightblue_bg = _create_color_wrappers('LIGHTBLUE_EX')
lightmagenta, lightmagenta_bg = _create_color_wrappers('LIGHTMAGENTA_EX')
lightcyan, lightcyan_bg = _create_color_wrappers('LIGHTCYAN_EX')
lightwhite, lightwhite_bg = _create_color_wrappers('LIGHTWHITE_EX')


def bold(*args):
    return ''.join((Style.BRIGHT, *args, Style.NORMAL))


CLEAR_EOL = '\033[0K'
