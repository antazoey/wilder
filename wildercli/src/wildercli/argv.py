import click
from wilder.config import create_config_object
from wilder.enum import AlbumState
from wilder.enum import AlbumType
from wilder.errors import NoArtistsFoundError
from wildercli.clickext.types import FileOrString
from wildercli.output_formats import OutputFormat
from wildercli.wild_factory import get_wilder


yes_option = click.option(
    "-y",
    "--assume-yes",
    is_flag=True,
    expose_value=False,
    callback=lambda ctx, param, value: ctx.obj.set_assume_yes(value),
    help='Assume "yes" as the answer to all prompts and run non-interactively.',
)
song_option = click.option(
    "-s", "--song", help="A path to a song.", type=FileOrString()
)
format_option = click.option(
    "-f",
    "--format",
    type=click.Choice(OutputFormat(), case_sensitive=False),
    help="The output format of the result. Defaults to table format.",
    default=OutputFormat.TABLE,
)
bio_option = click.option("--bio", "--biography", help="The artist biography.")


class CLIState:
    def __init__(self):
        self._sdk = None
        self._config = None
        self.assume_yes = False

    @property
    def wilder(self):
        if self._sdk is None:
            self._sdk = get_wilder()
        return self._sdk

    @property
    def config(self):
        if self._config is None:
            self._config = create_config_object()
        return self._config

    def get_artist(self, artist_arg=None):
        try:
            return self.wilder.get_artist(name=artist_arg)
        except NoArtistsFoundError:
            click.echo("No artists found.")
            exit(1)

    def set_assume_yes(self, param):
        self.assume_yes = param


pass_state = click.make_pass_decorator(CLIState, ensure=True)


def artist_name_option(required=True):
    return click.option("--artist", help="The name of an artist.", required=required)


def album_name_option(required=True):
    return click.option("--album", help="The name of an album.", required=required)


def description_option(_help):
    return click.option("--description", "--desc", help=_help)


def wild_options():
    def decorator(f):
        f = pass_state(f)
        return f

    return decorator


def album_options():
    def decorator(f):
        f = description_option(_help="A description for the album.")(f)
        f = click.option(
            "--album-type",
            help="The type of album.",
            type=click.Choice(AlbumType.choices()),
        )(f)
        f = click.option(
            "--status",
            help="The current status of the album.",
            type=click.Choice(AlbumState.choices()),
        )(f)
        return f

    return decorator


artist_name_arg = click.argument("artist-name")
album_name_arg = click.argument("album-name")
alias_arg = click.argument("alias")
