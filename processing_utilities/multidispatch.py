from functools import wraps
from collections import OrderedDict


def pattern_match(sig, instance):
    """
    Naive pattern matching implementation.

    :param sig: Possibly nested tuple of types, the string "ANY" will match any type
    :param instance: Arguments to be type checked
    :return: True if match succeeds, otherwise false
    """
    # TODO: Implement variable length arguments
    if len(sig) != len(instance):
        return False

    for expected, actual in zip(sig, instance):
        if isinstance(expected, tuple):
            submatch = pattern_match(expected, actual)
            if not submatch:
                return False
            continue
        if expected == "ANY":
            continue
        if isinstance(actual, expected):
            continue
        return False
    return True


def pmultidispatch(f):
    """
    Multiple dispatch implementation allowing for basic pattern matching.

    :Note:
        `pmultidispatch` is order sensitive. In the event that multiple registered
        handler functions would match the same input, the first registered handler will
        be selected.

    :param f: Function providing default implementation
    :return: Wrapped function with a `func.register` method for registering patterns.
    """
    registry = OrderedDict()
    default = f

    def resolve(*args, **kwargs):
        """Resolve which handler to select based upon args"""
        received = tuple(args)
        for sig, func in registry.items():
            if pattern_match(sig, received):
                return func
        return default

    @wraps(f)
    def dispatcher(*args, **kwargs):
        """Top level function"""
        func = resolve(*args, **kwargs)
        return func(*args, **kwargs)

    def register_sig(*typesig):
        typesig = tuple(typesig)

        def register_func(g):
            registry[typesig] = g
            return g                    # Return original function so that decorators can stack
        return register_func

    dispatcher.register = register_sig
    return dispatcher


def multidispatch(f):
    """
    Basic multidispatch implementation, may have better performance than pmultidispatch.

    :param f: Function providing default implementation
    :return: Wrapped function with a `func.register` method for registering type signatures
    """
    # Overview of implementation:
    #    - A function the user wishes to multidispatch is decorated with @multidispatch
    #    - Call to @multidispatch registers the first function f as default implementation
    #      and replaces it with a dispatcher function
    #    - The dispatcher function is augmented with a `.register` decorator
    #    - When the `.register` decorator is called, it captures it's arguments
    #      and returns a decorator.
    #    - The decorator takes a function and registers it with the dispatcher.
    registry = {'default': f}

    @wraps(f)
    def dispatcher(*args, **kwargs):
        """Top level function."""
        sig = tuple(type(arg) for arg in args)
        default = registry['default']
        func = registry.get(sig, default)
        return func(*args, **kwargs)

    def register_sig(*typesig):
        typesig = tuple(typesig)

        def register_func(g):
            registry[typesig] = g
            return g                             # Return original function so that decorators can stack
        return register_func

    dispatcher.register = register_sig
    return dispatcher

