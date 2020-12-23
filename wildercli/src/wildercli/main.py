import signal
import sys

import click


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

@click.command()
def play():
    """Plays"""


@click.group(cls=ExceptionHandlingGroup, context_settings=CONTEXT_SETTINGS, help=BANNER)
@sdk_options(hidden=True)
def cli(state):
    pass
   
cli.add_command(play)
