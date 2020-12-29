import click


name_arg = click.argument("name")
artist_arg = click.argument("artist", required=False, default="__ALL__")
