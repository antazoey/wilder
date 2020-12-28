import json
import os

import pytest
from wilder.constants import ARTISTS, DISCOGRAPHY, DESCRIPTION
from wilder.constants import BIO
from wilder.constants import NAME
from wilder.enum import AlbumType
from wilder.parser import parse_mgmt


@pytest.fixture()
def schema_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "test.mgmt.json")


@pytest.fixture()
def mock_mgmt_json(schema_path):
    with open(schema_path) as test_file:
        return json.load(test_file)


def test_parse_mgmt_parses_artist(schema_path, mock_mgmt_json):
    mgmt = parse_mgmt(mgmt_path=schema_path)
    assert len(mgmt.artists) == 1
    actual_artist = mgmt.artists[0]
    expected_artist = mock_mgmt_json[ARTISTS][0]
    assert actual_artist.name == expected_artist[NAME]
    assert actual_artist.bio == expected_artist[BIO]
    assert len(actual_artist.discography) == 1


def test_parse_mgmt_parses_album(schema_path, mock_mgmt_json):
    mgmt = parse_mgmt(mgmt_path=schema_path)
    assert len(mgmt.artists) == 1
    actual_album = mgmt.artists[0].discography[0]
    expected_album = mock_mgmt_json[ARTISTS][0][DISCOGRAPHY][0]
    assert actual_album.name == expected_album[NAME]
    assert actual_album.description == expected_album[DESCRIPTION]
    assert actual_album.artwork is None
    assert actual_album.album_type == AlbumType.EP
