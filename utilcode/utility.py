import time
from functools import wraps

def fps_counter(func):
    last_time = time.perf_counter()
    #@wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal last_time
        current_time = time.perf_counter()
        elapsed = current_time - last_time
        last_time = current_time
        fps = 1.0 / elapsed if elapsed > 0 else 0.0
        result = func(*args, **kwargs)
        return result, fps
    return wrapper
