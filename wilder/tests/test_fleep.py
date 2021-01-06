import wilder.fleep as fleep


def test_get_audio_file_info_when_wav_file_returns_info(test_wav_file_path):
    with open(test_wav_file_path, "rb") as file:
        info = fleep.get_audio_file_info(file.read(128))
    assert info.type == ""
    assert info.extension == ""
    assert info.mime == ""
