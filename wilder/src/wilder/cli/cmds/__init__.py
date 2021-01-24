import click
from PyInquirer import prompt
from wilder.lib.constants import Constants
from wilder.lib.mgmt.album_dir import get_album_directory


class AlbumDirCommand(click.Command):
    def invoke(self, ctx):
        wilder = ctx.obj.wilder  # This line must stay to load context
        album_arg = ctx.params.get(Constants.ALBUM)
        artist_arg = ctx.params.get(Constants.ARTIST)
        artist = wilder.get_artist(artist_arg)
        album_dir = get_album_directory(
            wilder, get_default_handler=lambda: _select_album_from_list(artist)
        )
        album_json = album_dir.get_album_json(artist_arg, album_arg)
        ctx.params[Constants.ALBUM] = album_json[Constants.NAME]
        ctx.params[Constants.ARTIST] = album_json[Constants.ARTIST]
        return super().invoke(ctx)


def _select_album_from_list(artist):
    # Gets called when not in an album directory
    albums = artist.get_discography()  # Errors when no albums
    if len(albums) == 1:
        album = albums[0]
    else:
        choices = [a.name for a in albums]
        album_name = _get_album_from_user_prompt(choices)
        album = artist.get_album_by_name(album_name)
    return album.to_json_for_album_dir()


def _get_album_from_user_prompt(choices):
    question = {
        "type": "list",
        "name": "choice",
        "message": "What album?",
        "choices": choices,
    }
    return prompt(question)["choice"]
