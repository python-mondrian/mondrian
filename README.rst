mondrian
========

Mondrian helps you paint your standard python logger.

.. image:: https://raw.githubusercontent.com/hartym/mondrian/master/demo.png
  :alt: Mondrian in action
  :width: 100%
  :align: center

Enabling mondrian is simple and straightforward:

.. code-block:: python

    import logging
    import mondrian

    logger = logging.getLogger()

    if __name__ == '__main__':
        mondrian.setup(excepthook=True)
        logger.setLevel(logging.INFO)

        logger.info('Hello, world.')

