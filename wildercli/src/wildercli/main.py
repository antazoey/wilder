import signal
import sys

import click

from wildercli.clickext.groups import ExceptionHandlingGroup
from wildercli.options import core_options

BANNER = """\b
.##......##.####.##.......########..########.########.
.##..##..##..##..##.......##.....##.##.......##.....##
.##..##..##..##..##.......##.....##.##.......##.....##
.##..##..##..##..##.......##.....##.######...########.
.##..##..##..##..##.......##.....##.##.......##...##..
.##..##..##..##..##.......##.....##.##.......##....##.
..###..###..####.########.########..########.##.....##
"""


# Handle KeyboardInterrupts by just exiting instead of printing out a stack
def exit_on_interrupt(signal, frame):
    click.echo(err=True)
    sys.exit(1)


signal.signal(signal.SIGINT, exit_on_interrupt)
CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "max_content_width": 200,
}


@click.group(cls=ExceptionHandlingGroup, context_settings=CONTEXT_SETTINGS, help=BANNER)
@core_options(hidden=True)
def cli(state):
    pass


cli.add_command(play)