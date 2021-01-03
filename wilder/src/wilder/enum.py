from wilder.util import get_attribute_keys_from_class


class AlbumState:
    IN_PROGRESS = "IN_PROGRESS"
    DEMO = "DEMO"
    PRE_RELEASE = "PRE_RELEASED"
    RELEASED = "RELEASED"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(AlbumState)


class AlbumType:
    SINGLE = "SINGLE"
    EP = "EP"
    LP = "LP"
    B_SIDES = "B-SIDES"
    GREATEST_HITS = "GREATEST_HITS"
    REMIX = "REMIX"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(AlbumType)


class ReleaseType:
    CENSORED = "CENSORED"
    EXTENDED = "EXTENDED"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(ReleaseType)
