import json
import os

import pytest
from wilder import parse_mgmt


@pytest.fixture()
def schema_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "mgmt.json")


@pytest.fixture()
def mock_mgmt_json(schema_path):
    with open(schema_path) as test_file:
        return json.load(test_file)


@pytest.fixture()
def parsed_mock_mgmt(mock_mgmt_json):
    return parse_mgmt(mock_mgmt_json)
