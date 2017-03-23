# Spark Bot Example

A simple Python 3 demo using AIOHTTP for asynchronous polling of Cisco Spark for messages.

## Install

`pip install -r requirements.txt`

## Configure

Set a file `config.yml` with the settings

```yaml
api_key: <api key>
default_room_id: <default room id>
```

## Run

Using Python 3 (3.5+)

`python bot.py`