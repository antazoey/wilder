from wilder.lib.constants import Constants


class Release:
    # The date of the release.
    release_date = None

    # The type of the release, such as EXTENDED.
    release_type = None

    # The artist name of the release.
    artist = None

    # the album name of the release.
    album = None

    @classmethod
    def from_json(cls, artist_name, album_name, release_json):
        release = Release()
        release.artist = artist_name
        release.album = album_name
        release.release_date = release_json.get(Constants.RELEASE_DATE)
        release.release_type = release_json.get(Constants.RELEASE_TYPE)
        return release

    def to_json(self):
        return {
            Constants.RELEASE_DATE: self.release_date,
            Constants.RELEASE_TYPE: self.release_type,
        }
