import aiohttp
import asyncio
import async_timeout
import requests
import arrow
import logging
import yaml

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig()

log = logging.getLogger(__name__)

MESSAGES_URL = 'https://api.ciscospark.com/v1/messages'
ROOMS_URL = 'https://api.ciscospark.com/v1/rooms'

# Configuration for me!
with open('config.yml') as conf_yml:
    config = yaml.load(conf_yml)

SPARK_API_KEY = config['api_key']
try:
    WHITELIST_ROOMS = config['rooms']
except KeyError:
    WHITELIST_ROOMS = False

_standard_headers = {
    'Authorization': 'Bearer {0}'.format(SPARK_API_KEY)
}


def handle_message(text, email):
    # This is where you would call your bot with the message..
    pass


def list_rooms(session):
    log.debug("Fetching rooms")
    response = requests.get(ROOMS_URL, headers=_standard_headers)
    response.raise_for_status()
    return response.json()


def get_room(session, room_id):
    log.debug("Get room")
    response = requests.get(ROOMS_URL + '/' + room_id, headers=_standard_headers)
    response.raise_for_status()
    return response.json()


async def fetch_messages(session, room):
    log.debug("Fetching messages for room {0}".format(room))
    with async_timeout.timeout(10):
        params = {'roomId': room}
        async with session.get(MESSAGES_URL, params=params,
                               headers=_standard_headers) as response:
            return await response.json()

# Messages we have heard
heard = []

async def main(start):
    tasks = []

    async with aiohttp.ClientSession() as session:
        if WHITELIST_ROOMS:
            rooms = [get_room(session, room_id) for room_id in WHITELIST_ROOMS]
        else:
            rooms = list_rooms(session)['items']

        room_data = [(room['id'], room['title'], room['lastActivity']) for room in rooms]
        
        # For each room, only ask if it has activity since the start of the application
        for room, name, lastActivity in room_data:
            if arrow.get(lastActivity) > start:
                log.debug("Checking room messages..")
                task = asyncio.ensure_future(fetch_messages(session, room))
                tasks.append(task)
            else:
                log.debug("No new activity on this room")

        # Wait for all rooms to respond
        responses = await asyncio.gather(*tasks)
        for messages in responses:
            for message in messages['items']:
                try:
                    text = message['text']
                except KeyError:
                    # File message
                    text = '<file>'
                date = arrow.get(message['created'])
                if date > start and message['id'] not in heard:
                    heard.append(message['id'])
                    print("{0} said {1}: {2}".format(message['personEmail'],
                                                 date.humanize(),
                                                 text))
                    handle_message(text, message['personEmail'])

start = arrow.utcnow()
loop = asyncio.get_event_loop()
print("Cisco Spark Async bot")
print("Listing rooms and messages..")
while True:
    future = main(start)
    loop.run_until_complete(future)
loop.close()