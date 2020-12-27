import click

from wildercli.clickext.types import FileOrString


class CLIState:
    def __init__(self):
        self._core = None
        self.assume_yes = False

    @property
    def core(self):
        if self._core is None:

            # TODO: replace with interface for C# package
            self._core = None

        return self._core

    def set_assume_yes(self, param):
        self.assume_yes = param


pass_state = click.make_pass_decorator(CLIState, ensure=True)


song_option = click.option("-s", "--song", help="A path to a song.", type=FileOrString())


def core_options(hidden=False):
    def decorator(f):
        f = pass_state(f)
        return f

    return decorator
