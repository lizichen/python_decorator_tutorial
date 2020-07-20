import functools

def do_twice(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)

    return wrapper_do_twice


@do_twice
def say_whee():
    print("Whee!")



say_whee()

print(say_whee.__name__)