# coding=utf-8

import osu_ds

osu = osu_ds.OsuApi(api_key="a134cfc8caf7c29c873272821051dbaea40db1eb")

ds = osu.get_user("DefaltSimon")

print(ds.name,
      ds.level,
      ds.playcount,
      ds.country_rank)
