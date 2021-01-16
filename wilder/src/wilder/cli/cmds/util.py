import click
from wilder.errors import ArtistNotFoundError
from wilder.errors import NoArtistsFoundError
from wilder.cli.output_formats import OutputFormatter


def echo_formatted_list(_format, _list, header=None):
    formatter = OutputFormatter(_format, header=header)
    formatter.echo_formatted_list(_list)


class ArtistArgRequiredIfGivenCommand(click.Command):
    def invoke(self, ctx):
        try:
            return super().invoke(ctx)
        except (ArtistNotFoundError, NoArtistsFoundError) as err:
            click.echo(str(err))
