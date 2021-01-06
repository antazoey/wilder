import click
from wilder.constants import Constants
from wildercli.argv import album_name_arg
from wildercli.argv import album_option
from wildercli.argv import artist_name_option
from wildercli.argv import format_option
from wildercli.argv import update_album_options
from wildercli.argv import wild_options
from wildercli.cmds.util import ArtistArgRequiredIfGivenCommand
from wildercli.cmds.util import echo_formatted_list
from wildercli.output_formats import OutputFormat
from wildercli.util import abridge


@click.group()
def album():
    """Tools for creating albums."""
    pass


@click.command(cls=ArtistArgRequiredIfGivenCommand)
@update_album_options()
def new(state, artist, album_name, description, album_type, status):
    """Start a new album."""
    state.wilder.start_new_album(
        album_name,
        artist_name=artist,
        description=description,
        album_type=album_type,
        status=status,
    )


ALBUM_HEADER = {
    Constants.NAME: "Name",
    Constants.DESCRIPTION: "Description",
    Constants.ALBUM_TYPE: "Album Type",
    Constants.STATUS: "Status",
}


@click.command(Constants.LIST, cls=ArtistArgRequiredIfGivenCommand)
@wild_options()
@artist_name_option
@format_option
def _list(state, artist, format):
    """List an artist's discography."""
    artist_obj = state.get_artist(artist)
    albums_json_list = [a.to_json() for a in artist_obj.discography]
    if not albums_json_list:
        _handle_no_albums_found(artist_obj.name)
        return

    if format == OutputFormat.TABLE:
        for alb in albums_json_list:
            full_desc = alb.get(Constants.DESCRIPTION)
            if full_desc:
                alb[Constants.DESCRIPTION] = abridge(full_desc)

    click.echo(f"Albums by '{artist_obj.name}':\n")
    echo_formatted_list(format, albums_json_list, header=ALBUM_HEADER)


@click.command(cls=ArtistArgRequiredIfGivenCommand)
@update_album_options()
def update(state, artist, album_name, description, album_type, status):
    """Update an album."""
    state.wilder.update_album(
        album_name,
        artist_name=artist,
        description=description,
        album_type=album_type,
        status=status,
    )


@click.command(cls=ArtistArgRequiredIfGivenCommand)
@wild_options()
@artist_name_option
@album_option(required=True)
@click.option("--track", "-t", help="The path to a track.", required=True)
def add_track(state, artist, album_name, track):
    pass


def _handle_no_albums_found(name):
    msg = f"{name} does not have any albums."
    click.echo(msg)


album.add_command(new)
album.add_command(_list)
album.add_command(update)
