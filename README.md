# Spark Bot Example

A simple Python 3 demo using AIOHTTP for asynchronous polling of Cisco Spark for messages.

The thread will get the time, get a list of rooms, then asynchronously get all new messages in every room
and print them on the screen.

You could use this for a simple message callback/bot function.

## Install

`pip install -r requirements.txt`

## Configure

Set a file `config.yml` with the settings

```yaml
api_key: <api key>
```

Optionally, you can set the list of rooms by ID

```yaml
rooms:
    - <rooom 1 id>
    - <room 2 id>
```

## Run

Using Python 3 (3.5+)

`python bot.py`