import time
from functools import wraps

from apple_health_parser.utils.logging import logger


def timeit(func):
    """
    Log (`log.info`) how long a function takes to run (in seconds).
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        logger.info(f"Took {time.time() - start:.2f} seconds to run {func.__name__}")
        return result

    return wrapper
