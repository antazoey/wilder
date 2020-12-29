import os
import signal
import sys

import click
from wildercli.clickext.groups import ExceptionHandlingGroup
from wildercli.cmds import config
from wildercli.cmds import artists
from wildercli.cmds import album
from wildercli.cmds import albums
from wildercli.cmds import play
from wildercli.cmds import sign
from wildercli.cmds import unsign
from wildercli.options import core_options


BANNER = """\b
 |#      |#   |#   |#      |#----#   |#-----  |#-----#
 |#  |#  |#   |#   |#      |#    ##  |#       |#    ##
 |#  |#  |#   |#   |#      |#    ##  |#       |#    ##
 |#  |#  |#   |#   |#      |#    ##  |#---    |#----#
 |#  |#  |#   |#   |#      |#    ##  |#       |#  ##
 |#  |#  |#   |#   |#      |#    ##  |#       |#   ##
 |#__# #__#   |#   |#____  |#____#   |#_____  |#    #__
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
cli.add_command(album)
cli.add_command(albums)
cli.add_command(artists)
cli.add_command(config)
cli.add_command(sign)
cli.add_command(unsign)
