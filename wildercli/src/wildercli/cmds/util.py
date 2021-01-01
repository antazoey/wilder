import click
from wilder.errors import ArtistNotFoundError
from wildercli.output_formats import OutputFormatter


def echo_formatted_list(_format, _list):
    formatter = OutputFormatter(_format)
    formatter.echo_formatted_list(_list)


def artist_arg_required_if_given():
    class ArtistArgRequiredIfGivenCommand(click.Command):
        def invoke(self, ctx):
            try:
                return super().invoke(ctx)
            except ArtistNotFoundError as err:
                click.echo(str(err))

    return ArtistArgRequiredIfGivenCommand
