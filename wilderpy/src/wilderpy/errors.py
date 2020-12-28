class WildError(Exception):
    """This base-error trips us all up."""


class ArtistAlreadySignedError(Exception):
    """An error raised when trying to sign an artist that is already signed."""


class ArtistNotFoundError(Exception):
    """An error raised when an artist is not found in the local mgmt.json file."""
