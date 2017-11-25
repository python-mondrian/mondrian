import os
import platform
import shlex
import struct
import subprocess
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


def get_size():
    """ getTerminalSize()
     - get width and height of console
     - works on linux,os x,windows,cygwin(windows)
     originally retrieved from:
     http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_size_tput()
            # needed for window's python in cygwin's xterm!
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_size_linux()
    if tuple_xy is None:
        tuple_xy = (80, 25)  # default value
    return tuple_xy


def _get_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        pass


def _get_size_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass


def _get_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])
