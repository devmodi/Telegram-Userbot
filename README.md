## Telegram Userbot

A simple telegram userbot based on telethon.

## Build

```
pip install poetry
poetry install
```

## Usage

First, you need to create a [telegram application](https://my.telegram.org/auth) and generate your api id and setup your [MongoDB](https://docs.atlas.mongodb.com/getting-started/) cluster.

Finally create a .env file in the root directory of the project folder to store the configs.

Your env file should look something like this:
```
API_ID=Your API ID
API_HASH=Your API HASH
SESSION=SESSION Name
CONNECTION_STRING=MongoDB Connection URL
```