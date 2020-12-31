import click
from wilder.errors import ArtistNotFoundError
from wildercli.output_formats import OutputFormatter


def echo_formatted_list(_format, _list):
    formatter = OutputFormatter(_format)
    formatter.echo_formatted_list(_list)


def artist_arg_required_if_given(artist_key="artist_name"):
    class ArtistArgRequiredIfGivenCommand(click.Command):
        def invoke(self, ctx):
            artist = ctx.params.get(artist_key)
            try:
                return super().invoke(ctx)
            except ArtistNotFoundError:
                click.echo(f"Artist '{artist}' not found.")

    return ArtistArgRequiredIfGivenCommand


def get_artist(mgmt, artist_name):
    return (
        mgmt.get_artist_by_name(artist_name) if artist_name else mgmt.get_focus_artist()
    )
