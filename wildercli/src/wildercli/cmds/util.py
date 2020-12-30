import click
from wilder.errors import ArtistNotFoundError
from wildercli.output_formats import OutputFormatter


def echo_formatted_list(_format, _list):
    formatter = OutputFormatter(_format)
    formatter.echo_formatted_list(_list)


def requires_existing_artist_if_given(f):
    def decorate(*args, **kwargs):
        artist = kwargs.get("artist")
        try:
            return f(*args, **kwargs)
        except ArtistNotFoundError:
            click.echo(f"Artist '{artist}' not found.")

    decorate.__doc__ = f.__doc__
    return decorate
