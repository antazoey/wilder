import click
from wilderpy.errors import ArtistNotFoundError
from wilderpy.mgmt import get_mgmt


@click.group()
def artist():
    """Manage your artists."""
    pass


@click.command()
@click.argument("name")
def get(name):
    """Get an artist by name."""
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
def create():
    """Create a new artist."""


artist.add_command(get)
artist.add_command(create)
