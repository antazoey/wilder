import os

from wilder.errors import InvalidAudioFileError
from wilder.errors import WildNotFoundError

"""
Forked from fleep library by Mykyta Paliienko (https://github.com/floyernick/fleep-py).
"""

AUDIO_FILE_DATA = [
    {
        "type": "audio",
        "extension": "midi",
        "mime": "audio/midi",
        "offset": 0,
        "signature": ["4D 54 68 64"],
    },
    {
        "type": "audio",
        "extension": "mp3",
        "mime": "audio/mpeg",
        "offset": 0,
        "signature": ["49 44 33"],
    },
    {
        "type": "audio",
        "extension": "m4a",
        "mime": "audio/mp4",
        "offset": 4,
        "signature": ["66 74 79 70 4D 34 41 20"],
    },
    {
        "type": "audio",
        "extension": "oga",
        "mime": "audio/ogg",
        "offset": 0,
        "signature": ["4F 67 67 53 00 02 00 00"],
    },
    {
        "type": "audio",
        "extension": "wav",
        "mime": "audio/wav",
        "offset": 0,
        "signature": ["52 49 46 46"],
    },
    {
        "type": "audio",
        "extension": "wma",
        "mime": "audio/x-ms-wma",
        "offset": 0,
        "signature": ["30 26 B2 75 8E 66 CF 11"],
    },
    {
        "type": "audio",
        "extension": "flac",
        "mime": "audio/flac",
        "offset": 0,
        "signature": ["66 4C 61 43 00 00 00 22"],
    },
    {
        "type": "audio",
        "extension": "mka",
        "mime": "audio/x-matroska",
        "offset": 31,
        "signature": ["6D 61 74 72 6F 73 6B 61"],
    },
    {
        "type": "audio",
        "extension": "au",
        "mime": "audio/basic",
        "offset": 0,
        "signature": ["2E 73 6E 64"],
    },
    {
        "type": "audio",
        "extension": "ra",
        "mime": "application/octet-stream",
        "offset": 0,
        "signature": ["2E 52 4D 46"],
    },
    {
        "type": "audio",
        "extension": "amr",
        "mime": "application/octet-stream",
        "offset": 0,
        "signature": ["23 21 41 4D"],
    },
    {
        "type": "audio",
        "extension": "ac3",
        "mime": "application/octet-stream",
        "offset": 0,
        "signature": ["0B 77"],
    },
    {
        "type": "audio",
        "extension": "voc",
        "mime": "application/octet-stream",
        "offset": 0,
        "signature": ["43 72 65 61 74 69 76 65"],
    },
    {
        "type": "video",
        "extension": "3g2",
        "mime": "video/3gpp2",
        "offset": 4,
        "signature": ["66 74 79 70 33 67 70"],
    },
    {
        "type": "video",
        "extension": "3gp",
        "mime": "video/3gpp",
        "offset": 4,
        "signature": ["66 74 79 70 33 67 70"],
    },
]


def get_audio_file_info(audio_file_path):
    """Determines file format and picks suitable file types, extensions and MIME types.

    Args:
        audio_file_path (str): The path to an audio file.

    Returns: Instance of wilder.fleep.Info.
    """
    builder = _InfoBuilder(audio_file_path)
    return builder.build()


class Info:
    """Information about the file.

    Args:
        _type (list): List of file types.
        extension (list): List of file extensions.
        mime (list): List of file MIME types.

    Returns: Instance of wilder.fleep.Info.
    """

    def __init__(self, _type, extension, mime):
        self.type = _type
        self.extension = extension
        self.mime = mime


class _InfoBuilder:
    _TYPE_KEY = "type"
    _EXT_KEY = "extension"
    _MIME_KEY = "mime"
    _KEYS = [_TYPE_KEY, _EXT_KEY, _MIME_KEY]

    def __init__(self, audio_file_path):
        self._path = audio_file_path
        self.info = {self._TYPE_KEY: {}, self._EXT_KEY: {}, self._MIME_KEY: {}}
        audio_bytes = _get_bytes(audio_file_path)
        self._stream = _get_stream(audio_bytes)

    def build(self):
        for element in AUDIO_FILE_DATA:
            for signature in element["signature"]:
                sig_len = len(signature)
                offset = element["offset"] * 2 + element["offset"]
                if signature == self._stream[offset : sig_len + offset]:
                    for key in self.keys:
                        self.info[key][element[key]] = sig_len
        if not self._is_audio():
            raise InvalidAudioFileError(self._path)
        return self._to_info()

    @property
    def keys(self):
        return self._KEYS

    @property
    def _type(self):
        return self.info[self._TYPE_KEY]

    @property
    def _ext(self):
        return self.info[self._EXT_KEY]

    @property
    def _mime(self):
        return self.info[self._MIME_KEY]

    def _is_audio(self):
        return self._type and self._ext and self._mime

    def _to_info(self):
        builder = {self._TYPE_KEY: [], self._EXT_KEY: [], self._MIME_KEY: []}
        for key in self.keys:
            builder[key] = [
                element
                for element in sorted(
                    self.info[key], key=self.info[key].get, reverse=True
                )
            ]
        _type = builder[self._TYPE_KEY]
        ext = builder[self._EXT_KEY]
        mime = builder[self._MIME_KEY]
        return Info(_type, ext, mime)


def _get_bytes(audio_file):
    if isinstance(audio_file, str):
        if os.path.isfile(audio_file):
            with open(audio_file, "rb") as aud_file:
                return aud_file.read(128)
        raise WildNotFoundError(f"No audio file found at path '{audio_file}'.")
    raise TypeError("Path must be a str.")


def _get_stream(audio_bytes):
    return " ".join(["{:02X}".format(byte) for byte in audio_bytes])
