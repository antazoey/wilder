import shutil

import click
from wilder.config import set_client_settings
from wilder.constants import Constants
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
        click.echo("Destroying now.")
        state.wilder.nuke()
        cli_proj_files_path = get_user_project_path()
        shutil.rmtree(cli_proj_files_path)


@click.command()
def set_test_server():
    """Use the local dev server config."""
    _set_test_server()


def _set_test_server():
    test_host = "http://127.0.0.1"
    test_port = 5000
    _json = {Constants.HOST: test_host, Constants.PORT: test_port}
    set_client_settings(_json)


dev.add_command(nuke)
dev.add_command(set_test_server)
