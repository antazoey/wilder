import click
from wildercli.cmds.mgmt.album import album
from wildercli.cmds.mgmt.artist import artist


@click.group()
def mgmt():
    """Manage your artists, albums, and tracks."""
    pass


mgmt.add_command(album)
mgmt.add_command(artist)
