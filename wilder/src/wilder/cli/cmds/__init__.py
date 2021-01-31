import click
from wilder.cli.select import get_user_selected_item
from wilder.lib.constants import Constants
from wilder.lib.mgmt.album_dir import get_album_directory_obj


class AlbumDirCommand(click.Command):
    def invoke(self, ctx):
        wilder = ctx.obj.wilder  # This line must stay to load context
        album_arg = ctx.params.get(Constants.ALBUM)
        artist_arg = ctx.params.get(Constants.ARTIST)
        artist = wilder.get_artist(artist_arg)
        album_dir_obj = get_album_directory_obj(
            wilder, get_default_handler=lambda: _select_album_from_list(artist)
        )
        album_json = album_dir_obj.get_album_json(artist_arg, album_arg)
        ctx.params[Constants.ALBUM] = album_json[Constants.NAME]
        ctx.params[Constants.ARTIST] = album_json[Constants.ARTIST]
        return super().invoke(ctx)


def _select_album_from_list(artist):
    # Gets called when not in an album directory
    albums = artist.get_discography()  # Errors when no albums
    choices = [a.name for a in albums]
    album_name = get_user_selected_item("What album?", choices)
    album = artist.get_album(album_name)
    return album.to_json_for_album_dir()
