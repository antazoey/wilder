# Temp file for tracking plans / ideas

## CLI Commands

### Creating albums and songs

This will create some sort of entry for a new album.
Name must be unique.

```bash
wild album new "Wilder's Greatest Hits"
```

This will list the songs on an album.

```bash
wild album list-songs "Wilder's Greatest Hits"
```

This will list all the current albums you have made with `wild`:

```bash
wild albums
```

This is how you add a song to wild.
Point it to a .flp song to link an existing one, else it will create a .flp template
Later, will support other DAWs like Ableton.

```bash
wild album add --album "Wilder's Greatest Hits" --project-file "path/to/file"  --artist "Wilder"
```

The command either needs a path to a project file or some way of knowing which type of project to create.
It can gather that information from a `.wildrc` file if it exists, or it will require an argument.
Arguments will always take precendence over the `.wildrc`, but the `.wildrc` is useful for
setting user-defaults.

```bash
wild album add --album "Wilder's Greatest Hits" --project-type "fl"
```

You may want to add artwork to an album.
It must be an image file.

```bash
wild album add-artwork --album "Wilder's Greatest Hits"  --image "path/to/image"
```

### Worth-it commands

#### Package

Make a zip containing all the artwork.

```bash
wild album package --album "Wilder's Greatest Hits" --out "~/wilder/AlbumZips/"
```

#### Drop

Converts project files into WAVs or MP3s.

```bash
wild album drop --album "Wilder's Greatest Hits" --format "mp3"
wild album drop-song --album "Wilder's Greatest Hits" --song "Dream Girl" --format "wav"
```

#### Play

We need to interface with VLC player and automatically play add an album, with artwork and evetything, to VLC,
which is useful to demonstrating what an album may look like, on Bandcamp or wherever.

If not currently dropped down, it will do that first.

Start off supporting an easy one, perhaps VLC, but later on support Apple music or any other player.

```bash
wild album play --album "Wilder's Greatest Hits" --player "vlc"
wild album play-song --album "Wilder's Greatest Hits" --player "vlc"
```

#### Lint

Lint your songs! This feature will use defaults but mostly be changed in `.wildrc` to meet
personal requirements.

For example, the lint report can mention if the song is exceeding

#### Release

Will require login or something.

```bash
wild album release --album "Wilder's Greatest Hits" --store "bandcamp"
```

#### Song Versioning

Sort of like `git` but with less commits.

```bash
wild album add-song --album "Wilder's Greatest Hits" --song "Dream Girl" --version-tag "Scary Mix"
```

If adding a song that already exists in the same album without specifying a unique version tag,
it will prompt you for a version tag.

The most recent version added is the default album version unles specified otherwise.

```bash
wild album set-release-version --album "Wilder's Greatest Hits" --song "Dream Girl" --version-tag "Main Mix"
```

#### Album Versioning

Link one album to another as a separate version, such as an instrumental version.

```bash
wild album add "Wilder's Greatest Instrumentals" --parent-album "Wilder's Greatest Hits"
```

#### Discography

Manage whole discographies.

```bash
wild discog --artist "Wilder"
wild discog --artist "Wilder" --show-unreleased
```

## .wildrc

Default project settings:

# Default tags
* artist  # the artist to use when creating a new album when not specifying
* player  # the play to play songs with when no other specified
* genre  # the genre to tag tracks with when not specified; leave blank to not use
* stores  # the stores to push tracks to; required auth

# Linting
* max_db_demo  # main max decibal bound, like "0"
* min_db_demo  # main min decibal bound, like "-10"
* avg_db_demo  # demo average decibal range, like "-6.5...-3.5"
* max_db_main  # main max decibal bound, like "0"
* min_db_main  # main min decibal bound, like "-10"
* avg_dv_main  # main average decibal range, like "-3.0...-1.0"

Have be settable via but also encourage manual editing.

```bash
wild settings set --key artist --value "Wilder"
wilder settings get -k player
```

## Electron App / Web App

Yes.
