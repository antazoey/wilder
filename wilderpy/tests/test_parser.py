import json
import os

import pytest
from wilder.constants import ARTISTS
from wilder.constants import BIO
from wilder.constants import DESCRIPTION
from wilder.constants import DISCOGRAPHY
from wilder.constants import NAME
from wilder.constants import TRACKS
from wilder.enum import AlbumState
from wilder.enum import AlbumType
from wilder.parser import parse_mgmt


@pytest.fixture()
def schema_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "mgmt.json")


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
    artist = mgmt.artists[0]
    actual_album = mgmt.artists[0].discography[0]
    expected_album = mock_mgmt_json[ARTISTS][0][DISCOGRAPHY][0]
    assert actual_album.artist == artist
    assert actual_album.name == expected_album[NAME]
    assert actual_album.description == expected_album[DESCRIPTION]
    assert actual_album.artwork is None
    assert actual_album.album_type == AlbumType.EP
    assert actual_album.state == AlbumState.IN_PROGRESS
    assert len(actual_album.tracks) == 3


def test_parse_mgmt_parses_tracks(schema_path, mock_mgmt_json):
    mgmt = parse_mgmt(mgmt_path=schema_path)
    actual_tracks = mgmt.artists[0].discography[0].tracks
    expected_tracks = mock_mgmt_json[ARTISTS][0][DISCOGRAPHY][0][TRACKS]
    assert len(actual_tracks) == len(expected_tracks) == 3
    actual_one = actual_tracks[0]
    actual_two = actual_tracks[1]
    actual_three = actual_tracks[2]
    expected_one = expected_tracks[0]
    expected_two = expected_tracks[1]
    expected_three = expected_tracks[2]

    _assert_equal_track(mgmt, actual_one, expected_one, 1)
    _assert_equal_track(mgmt, actual_two, expected_two, 2)
    _assert_equal_track(mgmt, actual_three, expected_three, 3)

    assert actual_one.collaborators == ["Demons and Daffodils"]
    assert not actual_two.collaborators
    assert not actual_three.collaborators


def _assert_equal_track(mgmt, actual, expected, num):
    artist = mgmt.artists[0]
    album = mgmt.artists[0].discography[0]
    assert actual.artist == artist
    assert actual.album == album
    assert actual.name == expected[NAME]
    assert actual.description is None
    assert actual.track_number == num
    return True
