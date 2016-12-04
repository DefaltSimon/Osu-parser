# coding=utf-8

import osu_ds

# You can get your api key from https://osu.ppy.sh/p/api
key = "api key here"

osu = osu_ds.OsuApi(api_key=key)
ds = osu.get_user("DefaltSimon")

print(ds.name,
      ds.level,
      ds.playcount,
      ds.country_rank,
      ds.profile_url)
