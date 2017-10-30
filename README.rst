mondrian
========

Mondrian helps you paint your standard python logger.

Demo:

.. code-block:: python

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

Result...

.. image:: https://raw.githubusercontent.com/hartym/mondrian/master/demo.png
  :alt: Mondrian in action
  :width: 100%
  :align: center

Done.

