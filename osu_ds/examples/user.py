# coding=utf-8

import osu_ds

osu = osu_ds.OsuApi(api_key="some_ley")

ds = osu.get_user("DefaltSimon")

print(ds.name,
      ds.level,
      ds.playcount,
      ds.country_rank)
