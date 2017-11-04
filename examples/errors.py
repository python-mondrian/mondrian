import sys

import mondrian
import logging

if __name__ == '__main__':
    mondrian.setup(excepthook=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.info('Just so you know...')

    try:
        raise RuntimeError('''Hello, exception!\nFoo bar baz''')
    except Exception as exc:
        logger.exception('This is the message', exc_info=sys.exc_info())

    raise ValueError('that is not caught...')
