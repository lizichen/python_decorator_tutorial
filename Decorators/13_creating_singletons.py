import functools


def singleton(cls):
    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance

    wrapper_singleton.instance = None
    return wrapper_singleton

@singleton
class TheOne:
    pass


first_one = TheOne()

second_one = TheOne()

print(first_one == second_one)