import logging

import mondrian


def do_log(logger):
    logger.critical("This is a critical error.")
    logger.error("This is an error.")
    logger.warning("This is a warning.")
    logger.info("This is an info.")
    logger.debug("This is a debug information.")


if __name__ == "__main__":
    mondrian.setup(excepthook=True)

    print("=== Logging using root logger, level=INFO ===")
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    do_log(root_logger)
    print()

    print("=== Logging using foo.bar logger, level=DEBUG ===")
    logger = logging.getLogger("foo.bar")
    logger.setLevel(logging.DEBUG)
    do_log(logger)
    print()

    print("=== Logging an exception ===")
    raise RuntimeError("Woops, something bad happened...")
