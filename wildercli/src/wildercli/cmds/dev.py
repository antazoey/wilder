import shutil

import click
from wildercli.argv import wild_options
from wildercli.argv import yes_option
from wildercli.util import does_user_agree
from wildercli.util import get_user_project_path


@click.group(hidden=True)
def dev():
    """Developer tools."""
    pass


@click.command()
@yes_option
@wild_options()
def nuke(state):
    """Delete everything stored in MGMT."""
    if does_user_agree("Are you sure you wish to destroy everything? "):
        state.wilder.nuke()
        cli_proj_files_path = get_user_project_path()
        shutil.rmtree(cli_proj_files_path)
        click.echo("RIP.")


dev.add_command(nuke)
