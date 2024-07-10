# Stream Support

Various Django apps to support my Twitch stream. 

## Prerequisites

* Postgresql 14 or newer
* Redis
* Python 3

## Setup (LOCAL/DEV ONLY)

* Create an empty database and user in Postgres called `streamsupport_development`
* Initialize a virtualenv
* Copy the file `.env.example` to `.env` and fill out the required environment variables
* Install dependencies `pip install -r requirements.txt`
* Run DB migrations: `python manage.py makemigrations && python manage.py migrate`

To run just the web server: `python manage.py runserver`
To run a web server and background worker (for scheduled refresh jobs): `honcho start`

## haloinfinite

Grab stats from 343's Halo Infinite API to analyze and display on stream.

### Setup

* Create a Microsoft Azure app with client ID/secret, set these values in `.env`
* Create a new `XBoxUser` record:
  + TODO
* To add an authenticated user:
  + `python manage.py get_xbox_refresh_token < XBoxUser.id >`
  + This will give you a URL to visit which will prompt you to authenticate your Microsoft account with the Azure app you created
  + After authorizing, it will redirect you to a broken `localhost` URL; grab the `code` querystring param from that URL and enter it in the command line prompt
  + Eventually I will automate this through the web server
* Refresh data
  + Run the commands in `haloinfinite/management/commands`; need to add a shortcut for all of these
* View overlay
  + Visit `http://127.0.0.1:8000/haloinfinite/overlays/ranked_slayer/<MY GAMERTAG>`

### TODO
