import click
from wilder.cli.argv import wild_options
from wilder.cli.argv import yes_option
from wilder.cli.util import does_user_agree
from wilder.lib.config import delete_config_if_exists
from wilder.lib.config import set_client_settings
from wilder.lib.constants import Constants


class ConfigRequiredCommand(click.Command):
    def invoke(self, ctx):
        _config = ctx.obj.config
        if not _config.is_using_config():
            click.echo("Not using config.")
            return
        super().invoke(ctx)


@click.group()
def config():
    """Adjust settings."""
    pass


@config.command("set")
@click.option("--port", "-p", help="The local port to  run the Wild server on.")
def _set(port):
    """Create a config file to re-use your Wilder connection parameters."""
    host = Constants.DEFAULT_HOST
    port = port or Constants.DEFAULT_PORT
    _json = {Constants.HOST: host, Constants.PORT: port}
    set_client_settings(_json)


@config.command(cls=ConfigRequiredCommand)
@wild_options()
def show(state):
    """Show the current client config settings."""
    click.echo(
        f"Host: {state.config.host}, "
        f"Port: {state.config.port}. "
        f"IsEnabled: {str(state.config.is_enabled)}"
    )


@config.command(cls=ConfigRequiredCommand)
@wild_options()
@yes_option
def reset(state):
    """Delete the config if it exists."""
    _prompt = "Are you sure you wish to delete your config (there is no undo)? "
    if does_user_agree(_prompt):
        delete_config_if_exists()


@config.command(cls=ConfigRequiredCommand)
def enable():
    """Enable the config."""
    _enable_or_disable(True)


@config.command(cls=ConfigRequiredCommand)
def disable():
    """Disable the config."""
    _enable_or_disable(False)


def _enable_or_disable(do_enable):
    set_client_settings({Constants.IS_ENABLED: do_enable})
