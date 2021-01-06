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


def get_audio_file_info(audio_bytes):
    """Determines file format and picks suitable file types, extensions and MIME types.

    Args:
        audio_bytes (bytes): Byte sequence (128 bytes are enough)

    Returns: Instance of wilder.fleep.Info.
    """

    if not isinstance(audio_bytes, bytes):
        raise TypeError("object type must be bytes")

    info = {"type": dict(), "extension": dict(), "mime": dict()}
    stream = " ".join(["{:02X}".format(byte) for byte in audio_bytes])

    for element in AUDIO_FILE_DATA:
        for signature in element["signature"]:
            offset = element["offset"] * 2 + element["offset"]
            if signature == stream[offset : len(signature) + offset]:
                for key in ["type", "extension", "mime"]:
                    info[key][element[key]] = len(signature)

    for key in ["type", "extension", "mime"]:
        info[key] = [
            element for element in sorted(info[key], key=info[key].get, reverse=True)
        ]

    return Info(info["type"], info["extension"], info["mime"])
