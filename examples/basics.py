import logging
import mondrian

def do_log(logger):
    logger.critical('This is a critical error.')
    logger.error('This is an error.')
    logger.warning('This is a warning.')
    logger.info('This is an info.')
    logger.debug('This is a debug information.')

if __name__ == '__main__':
    root_logger = mondrian.getLogger()

    print('=== Logging with root logger, level=INFO ===')
    root_logger.setLevel(logging.INFO)
    do_log(root_logger)

    logger = mondrian.getLogger('foo.bar')

    print('=== Logging with foo.bar logger, level=DEBUG ===')
    logger.setLevel(logging.DEBUG)
    do_log(logger)

    print('=== Logging with root logger, level unchanged ===')
    do_log(root_logger)
