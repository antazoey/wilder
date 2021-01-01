import json
import signal
import sys

import click
from wildercli.argv import wild_options
from wildercli.clickext.groups import ExceptionHandlingGroup
from wildercli.cmds import album
from wildercli.cmds import artist
from wildercli.cmds import config
from wildercli.cmds import play
from wildercli.cmds.dev import dev


BANNER = """\b
 |#  |#  |#  |#  |#      |#----#   |#----  |#-----#
 |#  |#  |#  |#  |#      |#    ##  |#      |#    ##
 |#  |#  |#  |#  |#      |#    ##  |#---   |#----#
 |#  |#  |#  |#  |#      |#    ##  |#      |#    ##
 |#__# #__#  |#  |#____  |#____#   |#____  |#     #_
"""


def exit_on_interrupt(signal, frame):
    """Handle KeyboardInterrupts by just exiting instead of printing out a stack."""
    click.echo(err=True)
    sys.exit(1)


signal.signal(signal.SIGINT, exit_on_interrupt)
CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "max_content_width": 200,
}


@click.group(cls=ExceptionHandlingGroup, context_settings=CONTEXT_SETTINGS, help=BANNER)
@wild_options()
def cli(state):
    """The Wild CLI."""
    pass


@click.command()
@wild_options()
def mgmt(state):
    """Show the full MGMT JSON blob."""
    _json = json.dumps(state.mgmt.get_mgmt_json(), indent=2)
    click.echo(_json)


cli.add_command(play)
cli.add_command(album)
cli.add_command(artist)
cli.add_command(config)
cli.add_command(mgmt)
cli.add_command(dev)
