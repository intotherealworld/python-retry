import functools
import logging


def _retry(f, exceptions=None, pre_handler=None, recover=None, max_attempts=2, allow_log=False):
    if not exceptions:
        exceptions = [Exception]

    if not isinstance(exceptions, list):
        exceptions = [exceptions]

    current_attempt = 0
    while current_attempt <= max_attempts:
        try:
            return f()
        except Exception as e:
            raisable = True
            for t in exceptions:
                if isinstance(e, t):
                    raisable = False

            if raisable:
                raise e

            current_attempt += 1
            if allow_log:
                logging.info(f'retried: {current_attempt}, {f}')
            if pre_handler and current_attempt < max_attempts:
                pre_handler()

    if recover:
        return recover()


def retryable(exceptions=None, max_attempts=2, pre_handler=None, recover=None, allow_log=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if pre_handler:
                handler = getattr(args[0], pre_handler)
            else:
                handler = None

            if recover:
                recover_fn = getattr(args[0], recover)
            else:
                recover_fn = None

            return _retry(
                functools.partial(func, *args, **kwargs),
                exceptions=exceptions,
                max_attempts=max_attempts,
                pre_handler=handler,
                recover=recover_fn,
                allow_log=allow_log,
            )

        return wrapper

    return decorator
