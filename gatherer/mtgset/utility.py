
def is_sequence(arg):
    """
    Check whether an argument is iterable, but not a string.\n
    :param arg: argument to check
    :return: True if the argument is a non-string, iterable.
    """
    return not(hasattr(arg, "strip") and
               (hasattr(arg, "__getitem__") or
               hasattr(arg, "__iter__")))
