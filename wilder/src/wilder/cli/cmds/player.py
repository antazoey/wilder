import click
from wilder.cli.argv import song_option


@click.command()
@song_option
def play():
    """Play tracks and albums."""
