import click
from wilder.config import delete_config_if_exists
from wilder.config import set_client_settings
from wilder.constants import Constants
from wildercli.argv import wild_options
from wildercli.argv import yes_option
from wildercli.util import does_user_agree


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


@click.command("set")
def _set():
    """Create a config file to re-use your Wilder connection parameters."""
    host = "http://127.0.0.1"
    port = 6660
    _json = {Constants.HOST: host, Constants.PORT: port}
    set_client_settings(_json)


@click.command(cls=ConfigRequiredCommand)
@wild_options()
def show(state):
    """Show the current client config settings."""
    click.echo(
        f"Host: {state.config.host}, "
        f"Port: {state.config.port}. "
        f"IsEnabled: {str(state.config.is_enabled)}"
    )


@click.command(cls=ConfigRequiredCommand)
@wild_options()
@yes_option
def reset(state):
    """Delete the config if it exists."""
    _prompt = "Are you sure you wish to delete your config (there is no undo)? "
    if does_user_agree(_prompt):
        delete_config_if_exists()


@click.command(cls=ConfigRequiredCommand)
def enable():
    """Enable the config."""
    _enable_or_disable(True)


@click.command(cls=ConfigRequiredCommand)
def disable():
    """Disable the config."""
    _enable_or_disable(False)


def _enable_or_disable(do_enable):
    set_client_settings({Constants.IS_ENABLED: do_enable})


config.add_command(_set)
config.add_command(show)
config.add_command(reset)
config.add_command(enable)
config.add_command(disable)
