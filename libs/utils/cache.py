from functools import lru_cache, wraps
from time import monotonic


def lru_cache_with_ttl(maxsize=128, typed=False, ttl=60):
    """Least-recently used cache with time-to-live (ttl) limit."""

    class Result:
        __slots__ = ("value", "death")

        def __init__(self, value, death):
            self.value = value
            self.death = death

    def decorator(func):
        @lru_cache(maxsize=maxsize, typed=typed)
        def cached_func(*args, **kwargs):
            value = func(*args, **kwargs)
            death = monotonic() + ttl
            return Result(value, death)

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = cached_func(*args, **kwargs)
            if result.death < monotonic():
                result.value = func(*args, **kwargs)
                result.death = monotonic() + ttl
            return result.value

        wrapper.cache_clear = cached_func.cache_clear
        return wrapper

    return decorator
