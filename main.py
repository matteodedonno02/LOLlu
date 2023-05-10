from config import ENDPOINT
from config import RIOT_KEY
from config import ENDPOINT2
from config import BOT_KEY
from config import CHAT_ID
from config import players
import requests
import telegram
import asyncio
import time
import threading

def main():
    players_ids = get_player_id_map(players)
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)
    tasks = []
    for player, id in players_ids.items():
        tasks.append(loop.create_task(send_msg(player, id)))
    loop.run_until_complete(asyncio.gather(*tasks))

async def send_msg(name, id):
    bot = telegram.Bot(BOT_KEY)
    is_playing = False
    while(True):
        if fetch_api(id):
            if not is_playing:
                await bot.send_message(CHAT_ID, "Che lollacciu! " + name + " sta scioca a LOL!")
                is_playing = True
        else:
            is_playing = False
        await asyncio.sleep(60)

def get_player_id_map(players):
    map = {}
    for player in players:
        response = requests.get(ENDPOINT2 + player + "?api_key=" + RIOT_KEY)
        data = response.json()
        map[player] = data["id"]
    return map

def fetch_api(id):
    response = requests.get(ENDPOINT + id + "?api_key=" + RIOT_KEY)
    print(response)
    if response.status_code == 200:
        return True
    else:
        return False

if __name__ == "__main__":
    main()
