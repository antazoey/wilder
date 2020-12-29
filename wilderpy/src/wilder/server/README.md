# Wild Server Resources

## /mgmt [GET]

Get full MGMT JSON

## /artists [GET]

List all artists

## /sign [POST]

Sign a new artist

Params:

```json
{
  "artist": "Name of artist"
}
```

## /unsign  [POST]

Stop managing an artist

Params:

```json
{
  "artist": "Name of aritst"
}
```

## <artist>/create-album [POST]

Create an album

Params:

```json
{
  "album": "Name of Album"
}
```
