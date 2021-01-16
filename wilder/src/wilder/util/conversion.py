def to_bool(val):
    """Converts some values to booleans.

    Return conditions:
        * val when val is a bool
        * True when val.lower() is in ["t", "true"]
        * True when val is 1
        * False when val.lower() is in ["f", "false"]
        * False when val is 0
        * None for everything else
    """
    if val is None:
        return None

    elif isinstance(val, bool):
        return val

    elif isinstance(val, str):
        val = val.lower()
        if val in ["t", "true"]:
            return True
        elif val in ["f", "false"]:
            return False

    elif isinstance(val, int):
        if val == 0:
            return False
        elif val == 1:
            return True
    return None


def to_int(val):
    """Converts some values to integers.

    Return conditions:
        * val when val is an int
        * int(val) when val is a numeric str
        * None for everything else
    """
    if val is None:
        return None
    elif isinstance(val, int):
        return val
    elif isinstance(val, str):
        if val.isnumeric():
            return int(val)
    return None
