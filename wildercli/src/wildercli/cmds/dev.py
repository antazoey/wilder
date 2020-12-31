import shutil

import click
from wildercli.argv import mgmt_options
from wildercli.argv import yes_option
from wildercli.logger import get_cli_error_log_path
from wildercli.util import does_user_agree
from wildercli.util import get_user_project_path


@click.command(hidden=True)
@yes_option
@mgmt_options()
def nuke(state):
    """Delete everything stored in MGMT."""
    if does_user_agree("Are you sure you wish to destroy everything? "):
        click.echo("Destroying now.")
        state.mgmt.nuke()
        cli_proj_files_path = get_user_project_path()
        shutil.rmtree(cli_proj_files_path)


@click.command(hidden=True)
@click.option(
    "--last-n-lines", "-l", help="The last number of lines to show.", default=10
)
def logs(last_n_lines):
    """Show the last n lines of the CLI error logs."""
    logs_path = get_cli_error_log_path()
    try:
        with open(logs_path) as log_file:
            lines = log_file.readlines()
            length = len(lines)
            for line in lines[length-last_n_lines:]:
                line_data = line.strip()
                if line_data:
                    click.echo(f"- {line_data}")
    except FileNotFoundError:
        return []
