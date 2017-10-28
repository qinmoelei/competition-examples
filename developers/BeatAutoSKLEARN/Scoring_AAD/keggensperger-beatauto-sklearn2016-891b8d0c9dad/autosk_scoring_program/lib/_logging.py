import logging
import sys


def get_logger():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(message)s')

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    root = logging.getLogger()
    root.handlers = [stdout_handler, stderr_handler]
    logger = logging.getLogger('beatautosklearn')
    # Disable unwanted output
    logging.getLogger('multiprocessing').addHandler(logging.NullHandler())
    logging.getLogger('pip').addHandler(logging.NullHandler())
    logging.getLogger('pip').propagate = False

    return logger