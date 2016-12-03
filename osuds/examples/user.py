# coding=utf-8

import osuds

osu = osuds.OsuApi(api_key="a134cfc8caf7c29c873272821051dbaea40db1eb")

ds = osu.get_user("DefaltSimon")

print(ds.name,
      ds.level,
      ds.playcount,
      ds.country_rank)
