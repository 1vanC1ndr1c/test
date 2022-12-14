import time
from typing import Callable


def time_size_cache(time_to_live: int = 5 * 60,
                    max_calls: int = 10) -> Callable:
    """
    Cache decorator function that caches a function for a 'time_to_live'
    period of until 'max_calls' number of calls - whichever comes first.

    Args:
        time_to_live: Number of seconds that a function is cached for
        max_calls: Maximum number of calls that can occur before recalling

    Returns:
        Wrapped function that will be checked for caching conditions on every
        subsequent call when the same arguments are passed to it
    """

    def _decorator(fn: Callable) -> Callable:
        results = {}
        times = {}
        calls = {}

        def _wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)

            if key not in results:  # If first call, save
                results[key] = fn(*args, **kwargs)
                times[key] = time.time() + time_to_live
                calls[key] = 0

            calls[key] += 1

            # If expired, reset
            if calls[key] > max_calls or times[key] < time.time():
                del results[key]
                del times[key]
                del calls[key]
                results[key] = fn(*args, **kwargs)
                times[key] = time.time() + time_to_live
                calls[key] = 0

            return results[key]

        return _wrapper

    return _decorator


@time_size_cache(time_to_live=5 * 60, max_calls=10)
def add_fn(a: int, b: int) -> int:
    """
    Super complex function that requires caching

    Args:
        a: First summand
        b: Second summand

    Returns:
        The result of summation of the input arguments
    """
    return a + b
