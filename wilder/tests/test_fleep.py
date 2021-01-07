import pytest
import wilder.fleep as fleep
from wilder.errors import InvalidAudioFileError
from wilder.errors import WildNotFoundError


def test_get_audio_file_info_when_wav_file_returns_info(test_wav_file_path):
    info = fleep.get_audio_file_info(test_wav_file_path)
    assert info.type == ["audio"]
    assert info.extension == ["wav"]
    assert info.mime == ["audio/wav"]


def test_get_audio_file_info_when_text_file_raises_error(test_mgmt_json_path):
    with pytest.raises(InvalidAudioFileError) as err:
        fleep.get_audio_file_info(test_mgmt_json_path)
    assert (
        str(err.value)
        == f"File at '{test_mgmt_json_path}' is not a supported audio file."
    )


def test_get_audio_file_info_when_file_does_not_exist_raises_error(test_mgmt_json_path):
    with pytest.raises(WildNotFoundError):
        fleep.get_audio_file_info("no")
