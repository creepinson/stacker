
import time
import threading
import functools

import tqdm


def provide_progress_bar(function, estimated_time, tstep=0.2, tqdm_kwargs={}, args=[], kwargs={}):
    """Tqdm wrapper for a long-running function
    args:
        function - function to run
        estimated_time - how long you expect the function to take
        tstep - time delta (seconds) for progress bar updates
        tqdm_kwargs - kwargs to construct the progress bar
        args - args to pass to the function
        kwargs - keyword args to pass to the function
    ret:
        function(*args, **kwargs)
    """
    ret = [None]  # Mutable var so the function can store its return value

    def myrunner(function, ret, *args, **kwargs):
        ret[0] = function(*args, **kwargs)

    thread = threading.Thread(target=myrunner, args=(
        function, ret) + tuple(args), kwargs=kwargs)
    pbar = tqdm.tqdm(total=estimated_time, **tqdm_kwargs)

    thread.start()
    while thread.is_alive():
        thread.join(timeout=tstep)
        pbar.update(tstep)
    pbar.close()
    return ret[0]


def progress_wrapped(estimated_time, tstep=0.2, tqdm_kwargs={}):
    """Decorate a function to add a progress bar"""
    def real_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            return provide_progress_bar(function, estimated_time=estimated_time, tstep=tstep, tqdm_kwargs=tqdm_kwargs, args=args, kwargs=kwargs)
        return wrapper
    return real_decorator
