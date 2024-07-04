# Stream Support

Various Django apps to support my Twitch stream. 

## haloinfinite

Grab stats from 343's Halo Infinite API to analyze and display on stream.

### Commands

**Get a refresh token for a user**

```sh
python manage.py get_xbox_refresh_token < XBoxUser.id >
```

**Refresh matches for a user**

```sh
python manage.py retrieve_matches < XBoxUser.id >
```

**Refresh match stats for a user**

```sh
python manage.py retrieve_match_stats < XBoxUser.id >
```
