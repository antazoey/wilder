import click
from wilder.errors import ArtistNotFoundError
from wildercli.output_formats import OutputFormatter


def echo_formatted_list(_format, _list):
    formatter = OutputFormatter(_format)
    formatter.echo_formatted_list(_list)


def artist_arg_required_if_given(artist_key):
    class ArtistArgRequiredIfGivenCommand(click.Command):
        def invoke(self, ctx):
            artist = ctx.params.get(artist_key)
            try:
                return super().invoke(ctx)
            except ArtistNotFoundError:
                click.echo(f"Artist '{artist}' not found.")
    return ArtistArgRequiredIfGivenCommand
