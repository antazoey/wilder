import click
from wilder.lib.constants import Constants
from wilder.lib.errors import ArtistNotFoundError
from wilder.lib.errors import NoArtistsFoundError
from wilder.lib.mgmt.album_dir import get_album_json


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
        ctx.params[Constants.ALBUM] = ctx.obj.album_json[Constants.NAME]
        ctx.params[Constants.ARTIST] = ctx.obj.album_json[Constants.ARTIST]
        return super().invoke(ctx)
