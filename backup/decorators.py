from time import time

def timed(function):
    def wrapper(*args, **kwargs):
        before = time()
        value = function(*args, **kwargs)
        after = time()
        func_name = function.__name__
        print(f"{func_name}  took {after - before} seconds")
    return wrapper