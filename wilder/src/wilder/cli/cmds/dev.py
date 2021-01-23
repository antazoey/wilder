import click
from wilder.cli.argv import wild_options
from wilder.cli.argv import yes_option
from wilder.cli.util import does_user_agree
from wilder.cli.util import get_user_project_path
from wilder.lib.util.sh import remove_directory


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
        remove_directory(cli_proj_files_path)
        click.echo("RIP.")


dev.add_command(nuke)
