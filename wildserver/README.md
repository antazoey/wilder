# Wild Server

## Endpoints

### /

- `/mgmt` Get the full MGMT JSON.

### /artist

- `/artist/list`   : Get all artists.
- `/artist`        : Get an artist
- `/artist/focus`  : Change the focus artist.
- `/artist/sign`   : Sign a new artist.
- `/artist/unsign` : Remove a managed artist.
- `/artist/update` : Update artist information.
- `/artist/rename` : Rename an artist.
- `/artist/alias`  : Add, remove, or retrieve artist aliases.

### /album

- `/album/discrography`          : Get all albums for an artist.
- `/album/create`                : Create a new album.
- `/album/discography/<album>`   : Get an album.
- `/album/discography/add-track` : Add a track to an album.
