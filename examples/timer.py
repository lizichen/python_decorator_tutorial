import time

def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 'time')
        return result
    return f_timer


# Run a test example:
def get_number():
    for x in range(5000000):
        yield x


@timefunc
def expensive_function():
    for x in get_number():
        i = x ^ x ^ x
    return 'some result!'

result = expensive_function()