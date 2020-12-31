import click
from wildercli.clickext.types import FileOrString
from wildercli.mgmt_factory import get_wilder_mgmt
from wildercli.output_formats import OutputFormat


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
bio_option = click.option("--bio", help="The artist biography.")


class CLIState:
    def __init__(self):
        self._mgmt = None
        self.assume_yes = False

    @property
    def mgmt(self):
        if self._mgmt is None:
            self._mgmt = get_wilder_mgmt()
        return self._mgmt

    def get_artist(self, artist_arg):
        return (
            self.mgmt.get_artist_by_name(artist_arg)
            if artist_arg
            else self.mgmt.get_focus_artist()
        )

    def set_assume_yes(self, param):
        self.assume_yes = param


pass_state = click.make_pass_decorator(CLIState, ensure=True)


def artist_name_option(required=True):
    return click.option("--artist", help="The name of an artist.", required=required)


def album_name_option(required=True):
    return click.option("--album", help="The name of an album.", required=required)


def mgmt_options(hidden=False):
    def decorator(f):
        f = pass_state(f)
        return f

    return decorator


artist_name_arg = click.argument("artist-name")
album_name_arg = click.argument("album-name")
