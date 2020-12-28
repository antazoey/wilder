import click
from wildercli.options import song_option


@click.command()
@song_option
def play():
    """Play tracks and albums."""
