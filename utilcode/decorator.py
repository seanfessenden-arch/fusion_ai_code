#!/bin/python
import logging

def my_decorator(function):
    def wrapper(*args, **kwsrgs):
        print(f"I am the decorator {args}")
        function(*args, **kwsrgs)
    return wrapper

def my_decorator2(function):
    def wrapper(*args, **kwsrgs):
        return_val = function(*args, **kwsrgs)
        return f"I am the decorator2 {args}", return_val
    return wrapper

#---------------
@my_decorator
def func_to_decorate(msg):
    print(f"Being decorated {msg}")

@my_decorator2
def func_to_decorate2(msg):
    return f"Being decorated2 {msg}"

#func_to_decorate("by Bob")
results = func_to_decorate2("by Bob2")
print(results[0], results[1])
