import click
from wilder.errors import ArtistNotFoundError
from wilder.mgmt import get_mgmt
from wildercli.args import name_arg
from wildercli.options import format_option
from wildercli.output_formats import OutputFormatter


@click.group()
def artist():
    """Tools for managing artists."""
    pass


@click.command()
@name_arg
def get(name):
    """Get artist info by name."""
    mgmt = get_mgmt()
    try:
        return mgmt.get_artist_by_name(name)
    except ArtistNotFoundError:
        msg = (
            f"I'm sorry, we have no records of the artist '{name}'. "
            f"Do you care to sign an artist by this name? "
            f"Do so with:\n\twild mgmt artist sign [NAME]"
        )
        click.echo(msg, err=True)


@click.command()
@format_option
def artists(format):
    """List all your artists."""
    mgmt = get_mgmt()
    artists_to_list = [{"Name": a.name, "Bio": a.bio} for a in mgmt.artists]
    if not artists_to_list:
        click.echo("There are no artists currently being managed.")
    else:
        formatter = OutputFormatter(format)
        formatter.echo_formatted_list(artists_to_list)


artist.add_command(get)
