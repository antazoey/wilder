import json
import os
import shutil

from wilder.lib.constants import Constants as Consts

_PADDING_SIZE = 3


def noop(thing):
    return thing


def get_attribute_keys_from_class(cls):
    """Returns attribute names for the given class.

    Args:
        cls (class): The class to obtain attributes from.

    Returns:
        (list): A list containing the attribute names of the given class.
    """
    return [
        cls().__getattribute__(attr)
        for attr in dir(cls)
        if not callable(cls().__getattribute__(attr)) and not attr.startswith("_")
    ]
