import click
from wildercli.clickext.types import FileOrString
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


class CLIState:
    def __init__(self):
        self._core = None
        self.assume_yes = False

    @property
    def core(self):
        if self._core is None:

            # TODO: replace with interface for C# package
            self._core = None

        return self._core

    def set_assume_yes(self, param):
        self.assume_yes = param


pass_state = click.make_pass_decorator(CLIState, ensure=True)


def artist_option(required=True):
    return click.option(
        "--artist", help="The name of an artist.", required=required
    )


def album_option(required=True):
    return click.option(
        "--album", help="The name of an album.", required=required
    )


def core_options(hidden=False):
    def decorator(f):
        f = pass_state(f)
        return f

    return decorator
