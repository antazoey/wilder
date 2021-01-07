import json
import os

import pytest
from wilder import parse_mgmt

HERE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture()
def test_mgmt_json_path():
    return os.path.join(HERE, "testfiles/mgmt.json")


@pytest.fixture()
def test_mgmt_json(test_mgmt_json_path):
    with open(test_mgmt_json_path) as test_file:
        return json.load(test_file)


@pytest.fixture()
def test_wav_file_path():
    return os.path.join(HERE, "testfiles/test.wav")


@pytest.fixture()
def parsed_test_mgmt(test_mgmt_json):
    return parse_mgmt(test_mgmt_json)
