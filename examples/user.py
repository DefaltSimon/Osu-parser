# coding=utf-8
import asyncio
import osu_ds

# You can get your api key from https://osu.ppy.sh/p/api
key = "api key here"

osu = osu_ds.OsuApi(api_key=key)
loop = asyncio.get_event_loop()

async def show_user_info(name):
    ds = await osu.get_user(name)

    print(ds.name,
          ds.level,
          ds.playcount,
          ds.country_rank,
          ds.avatar_url)

loop.run_until_complete(show_user_info("DefaltSimon"))
