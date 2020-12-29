class BaseWildApi:

    @property
    def artists(self):
        """Override"""
        return []
    
    @property
    def artist_names(self):
        """The names of the artists represented."""
        return [a.name for a in self.artists]

    def is_represented(self, name):
        """Returns True if the artist is represented by Wilder."""
        return name in self.artist_names
