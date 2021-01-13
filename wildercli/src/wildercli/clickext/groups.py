import difflib
import re
from collections import OrderedDict

import click
from wilder.errors import AlbumAlreadyExistsError
from wilder.errors import AlbumNotFoundError
from wilder.errors import ArtistAlreadySignedError
from wilder.errors import ArtistNotFoundError
from wilder.errors import ArtistNotSignedError
from wildercli.errors import LoggedCLIError
from wildercli.errors import WilderCLIError
from wildercli.logger import get_main_cli_logger

_DIFFLIB_CUT_OFF = 0.6


class ExceptionHandlingGroup(click.Group):
    """A `click.Group` subclass to add custom exception handling."""

    logger = get_main_cli_logger()
    _original_args = None

    def make_context(self, info_name, args, parent=None, **extra):

        # grab the original command line arguments for logging purposes
        self._original_args = " ".join(args)

        return super().make_context(info_name, args, parent=parent, **extra)

    def invoke(self, ctx):
        try:
            return super().invoke(ctx)

        except click.UsageError as err:
            self._suggest_cmd(err)

        except LoggedCLIError:
            raise

        except (
            AlbumNotFoundError,
            ArtistNotSignedError,
            ArtistAlreadySignedError,
            ArtistNotFoundError,
            AlbumAlreadyExistsError,
        ) as err:
            click.echo(str(err))

        except WilderCLIError as err:
            self.logger.log_error(str(err))
            raise

        except click.ClickException:
            raise

        except click.exceptions.Exit:
            raise

        except OSError:
            raise

        except Exception:
            self.logger.log_verbose_error()
            raise LoggedCLIError("Unknown problem occurred.")

    @staticmethod
    def _suggest_cmd(usage_err):
        """Handles fuzzy suggestion of commands that are close to the bad command entered."""
        if usage_err.message is not None:
            match = re.match("No such command '(.*)'.", usage_err.message)
            if match:
                bad_arg = match.groups()[0]
                available_commands = list(usage_err.ctx.command.commands.keys())
                suggested_commands = difflib.get_close_matches(
                    bad_arg, available_commands, cutoff=_DIFFLIB_CUT_OFF
                )
                if not suggested_commands:
                    raise usage_err
                usage_err.message = "No such command '{}'. Did you mean {}?".format(
                    bad_arg, " or ".join(suggested_commands)
                )
        raise usage_err


class OrderedGroup(click.Group):
    """A `click.Group` subclass that uses an `OrderedDict` to store commands so the help text lists
    them in the order they were defined/added to the group.
    """

    def __init__(self, name=None, commands=None, **attrs):
        super().__init__(name, commands, **attrs)
        # the registered subcommands by their exported names.
        self.commands = commands or OrderedDict()

    def list_commands(self, ctx):
        return self.commands
