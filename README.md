# Stream Support

Various Django apps to support my Twitch stream. 

## haloinfinite

Grab stats from 343's Halo Infinite API to analyze and display on stream.

### Commands

**Get a refresh token for a user**

Need to do this when setting up (until I get the OAuth flow baked in).

```sh
python manage.py get_xbox_refresh_token < XBoxUser.id >
```
