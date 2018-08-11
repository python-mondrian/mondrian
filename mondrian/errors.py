import logging
import threading


def _get_error_message(exc):
    if hasattr(exc, "__str__"):
        message = str(exc)
        return message[0].upper() + message[1:]
    return ("\n".join(exc.args),)


def excepthook(exctype, exc, traceback, level=logging.CRITICAL, logger=None, context=None):
    """
    Error handler. Whatever happens in a plugin or component, if it looks like an exception, taste like an exception
    or somehow make me think it is an exception, I'll handle it.

    :param exc: the culprit
    :param trace: Hercule Poirot's logbook.
    :return: to hell
    """

    context = context or "thread {}".format(threading.get_ident())
    return (logger or logging.getLogger()).log(
        level,
        "Uncaught exception{}.".format(" (in {})".format(context) if context else ""),
        exc_info=(exctype, exc, traceback),
    )
