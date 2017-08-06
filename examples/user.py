# coding=utf-8
import asyncio
import osu_ds

import time
import configparser

parser = configparser.ConfigParser()
parser.read("config.ini")

# You can get your api key from https://osu.ppy.sh/p/api
key = parser.get("osu", "key")

osu = osu_ds.OsuApi(api_key=key)
loop = asyncio.get_event_loop()

async def show_user_info(name):
    t = time.clock()

    ds = await osu.get_user(name)

    print("Search took {}".format(time.clock() - t))

    s = """Name: {} (id:{})
Level: {}
Playcount: {}
Accuracy: {} %
Score: {} (ranked), {} (total)
PP: {}
Rank: {} (world), {} (country)
Amounts: {} (ss), {} (s), {} (a)
Country: {}

Urls:
    {} (profile)
    {} (avatar)
""".format(ds.name, ds.id, ds.level, ds.playcount, ds.accuracy,
           ds.ranked_score, ds.total_score, ds.pp, ds.world_rank, ds.country_rank,
           ds.ss_amount, ds.s_amount, ds.a_amount, ds.country, ds.profile_url, ds.avatar_url)

    print(s)

while True:
    name = input(">")
    loop.run_until_complete(show_user_info(name))
