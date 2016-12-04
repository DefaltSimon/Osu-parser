# coding=utf-8
from .errors import InvalidParameter

# Class types for osu!parser

# For convenience


class Transcribes:
    user_transcribe = {
        "user_id": "id",
        "username": "name",
        "pp_raw": "pp",
        "pp_rank": "world_rank",
        "pp_country_rank": "country_rank",
        "count_rank_ss": "ss_amount",
        "count_rank_s": "s_amount",
        "count_rank_a": "a_amount",
    }


class User(object):
    __slots__ = (
        "id", "name", "playcount", "ranked_score", "total_score",
        "pp", "world_rank", "country_rank", "level", "accuracy", "ss_amount", "s_amount",
        "a_amount", "events", "country", "profile_url", "avatar_url",
    )

    def __init__(self, data):
        if not isinstance(data, dict):
            raise InvalidParameter("Expected dict for data, got {}".format(type(data).__name__))

        for key, value in data.items():
            # Transcribe values from user_transcribe and
            # ignore invalid values
            if key not in User.__slots__:
                if key in Transcribes.user_transcribe.keys():
                    key = Transcribes.user_transcribe.get(key)

                else:
                    continue

            self.__setattr__(key, value)
