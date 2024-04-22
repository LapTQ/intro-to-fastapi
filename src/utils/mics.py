from functools import wraps
import time


def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print('[Execution time] {}: {}s'.format(f.__name__, end - start))
        return result
    return wrapper