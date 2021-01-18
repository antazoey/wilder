import os

import click
from wilder.cli.output_formats import OutputFormatter
from wilder.lib.constants import Constants
from wilder.lib.errors import ArtistNotFoundError
from wilder.lib.errors import NoArtistsFoundError
from wilder.lib.errors import NotInAlbumError
from wilder.lib.mgmt.album_dir import get_album_dir_json_path
from wilder.lib.util.sh import load_json_from_file


def echo_formatted_list(_format, _list, header=None):
    formatter = OutputFormatter(_format, header=header)
    formatter.echo_formatted_list(_list)


class ArtistArgRequiredIfGivenCommand(click.Command):
    def invoke(self, ctx):
        try:
            return super().invoke(ctx)
        except (ArtistNotFoundError, NoArtistsFoundError) as err:
            click.echo(str(err))


class AlbumDirCommand(ArtistArgRequiredIfGivenCommand):
    def invoke(self, ctx):
        # Load the MGMT data to auto-correct prior to context verification.
        wilder = ctx.obj.wilder
        album_arg = ctx.params.get(Constants.ALBUM)
        artist_arg = ctx.params.get(Constants.ARTIST)
        ctx.obj.album_json = get_album_json(wilder, artist_arg, album_arg)
        return super().invoke(ctx)


def get_album_json(wilder, artist_arg, album_arg):
    if not album_arg:
        here = os.getcwd()
        album_json_path = get_album_dir_json_path(here)
        if not os.path.isfile(album_json_path):
            raise NotInAlbumError()
        return load_json_from_file(album_json_path)
    else:
        album = wilder.get_album(album_arg, artist_name=artist_arg)
        return load_json_from_file(album.dir_json_path)


def get_artist_and_album(state, artist_arg, album_arg):
    # Artist/album args get set to album_json if provided
    _ = artist_arg
    _ = album_arg
    artist = state.album_json.get(Constants.ARTIST)
    album = state.album_json.get(Constants.NAME)
    return artist, album
