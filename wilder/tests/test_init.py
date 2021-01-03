from wilder import get_wilder_sdk
from wilder import parse_mgmt
from wilder.constants import Constants
from wilder.enum import AlbumState
from wilder.enum import AlbumType


def test_get_wilder_sdk_returns_object_with_expected_props(parsed_mock_mgmt):
    wilder = get_wilder_sdk(parsed_mock_mgmt)
    assert wilder.get_mgmt_json() == parsed_mock_mgmt.to_json


def test_parse_mgmt_parses_last_updated(schema_path, mock_mgmt_json):
    mgmt = parse_mgmt(mock_mgmt_json)
    assert mgmt.last_updated == 1234


def test_parse_mgmt_parses_focus_artist(schema_path, mock_mgmt_json):
    mgmt = parse_mgmt(mock_mgmt_json)
    assert mgmt.focus_artist == "Wilder"


def test_parse_mgmt_parses_artist(schema_path, mock_mgmt_json):
    mgmt = parse_mgmt(mock_mgmt_json)
    assert len(mgmt.artists) == 1
    actual_artist = mgmt.artists[0]
    expected_artist = mock_mgmt_json[Constants.ARTISTS][0]
    assert actual_artist.name == expected_artist[Constants.NAME]
    assert actual_artist.bio == expected_artist[Constants.BIO]
    assert actual_artist.also_known_as == expected_artist[Constants.ALSO_KNOWN_AS]
    assert len(actual_artist.discography) == 1


def test_parse_mgmt_parses_album(schema_path, mock_mgmt_json):
    mgmt = parse_mgmt(mock_mgmt_json)
    artist = mgmt.artists[0]
    actual_album = mgmt.artists[0].discography[0]
    expected_album = mock_mgmt_json[Constants.ARTISTS][0][Constants.DISCOGRAPHY][0]
    assert actual_album.artist == artist.name
    assert actual_album.name == expected_album[Constants.NAME]
    assert actual_album.description == expected_album[Constants.DESCRIPTION]
    assert actual_album.artwork is None
    assert actual_album.album_type == AlbumType.EP
    assert actual_album.state == AlbumState.IN_PROGRESS
    assert len(actual_album.tracks) == 3


def test_parse_mgmt_parses_tracks(schema_path, mock_mgmt_json):
    mgmt = parse_mgmt(mock_mgmt_json)
    actual_tracks = mgmt.artists[0].discography[0].tracks
    expected_tracks = mock_mgmt_json[Constants.ARTISTS][0][Constants.DISCOGRAPHY][0][
        Constants.TRACKS
    ]
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
    assert actual.artist == artist.name
    assert actual.album == album.name
    assert actual.name == expected[Constants.NAME]
    assert actual.description is None
    assert actual.track_number == num
    return True
