import pytest
from click.testing import CliRunner
from wildercli.argv import CLIState


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli_state(mocker, sdk, profile):
    mock_state = mocker.MagicMock(spec=CLIState)
    mock_state._sdk = sdk
    mock_state.profile = profile
    mock_state.search_filters = []
    mock_state.assume_yes = False
    return mock_state
