from functools import wraps
from django.core.cache import cache


def cached(timeout):
    def decorator(f):
        @wraps(f)
        def wrapper(*args):
            key = '%s.%s %r' % (f.__module__, f.__name__, args)
            rv = cache.get(key)
            if rv is None:
                rv = f(*args)
                cache.set(key, rv, timeout=timeout)
            return rv
        return wrapper
    return decorator
