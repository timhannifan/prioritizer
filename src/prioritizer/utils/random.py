import inspect
import random


FLOAT_TO_INT_MULTIPLIER = 2000000000

def generate_python_random_seed():
    """Generate a random integer suitable for seeding the Python random generator
    """
    return int(random.uniform(0, 1.0) * FLOAT_TO_INT_MULTIPLIER)


def classpath(klass):
    """Return the full class path

    Args:
        klass (class): A class
    """
    return f"{klass.__module__}.{klass.__name__}"


def bind_kwargs(kallable, **kwargs):
    """Bind keyword arguments to a callable and return as a dictionary

    Args:
        callable (callable): any callable
        **kwargs: keyword arguments to bind

    Returns: (dict)
    """
    call_signature = inspect.signature(kallable).bind_partial(**kwargs).arguments
    if 'kwargs' in call_signature:
        passed_kwargs = call_signature['kwargs']
    else:
        passed_kwargs = call_signature
    return passed_kwargs
