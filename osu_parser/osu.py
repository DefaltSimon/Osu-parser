# coding=utf-8

import time
import os
import logging

try:
    from selenium import webdriver
except ImportError:
    webdriver = None

from urllib.request import urlopen
from bs4 import BeautifulSoup

__author__ = "DefaltSimon"
__version__ = "0.2"
__license__ = "MIT"

things = [
    "  ",
    "\n",
    "\t",
    "\r"
]

user_search = "https://osu.ppy.sh/u/"
beatmap_search = "https://osu.ppy.sh/p/beatmaplist?q="

url_encode = lambda a: str(a).replace(" ", "%20")

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Exception


class OsuParserError(Exception):
    pass

# Utilities and Handlers


def clean(text):
    for ch in things:
        text = str(text).replace(ch, "")
    return text.strip(" ").strip("\n")


def handle_exceptions(fn):
    def handle(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except:
            log.error("Something went wrong while executing function {}".format(fn.__name__))
            raise OsuParserError("could not finish {}".format(fn.__name__))

    return handle


def phantom_in_path(path):
    return os.path.isfile(path)


class User(object):
    """
    A user on osu.ppy.sh/u/
    """
    def __init__(self, **kwargs):
        """
        Initializes all data.
        Missing data is None (of selenium was set to False when fetching).
        :param kwargs: kwargs
        """
        self.username = kwargs.get("username")
        self.age = kwargs.get("age")

        self.occupation = kwargs.get("occupation")
        self.country = kwargs.get("country")

        self.date_joined = kwargs.get("date_joined")
        self.date_active = kwargs.get("date_active")

        self.rank_world = kwargs.get("rank_world")
        self.rank_country = kwargs.get("rank_country")

        self.performance = kwargs.get("performance")
        self.level = kwargs.get("level")

        self.hit_accuracy = kwargs.get("hit_accuracy")
        self.total_hits = kwargs.get("total_hits")

        self.play_count = kwargs.get("play_count")
        self.play_time = kwargs.get("play_time")

        self.ranked_score = kwargs.get("ranked_score")
        self.total_score = kwargs.get("total_score")

        self.max_combo = kwargs.get("max_combo")


class OsuParser:
    """
    Osu! python library
    This library is in no way affiliated with Osu! or peppy.
    """
    def __init__(self, selenium_path="phantomjs", max_cache_age=43200):  # 12 hours
        self.cache = {}
        self.ages = {}

        self.max_age = max_cache_age

        self.selenium_available = bool(webdriver)
        self.selenium_path = selenium_path

        self.pjs = webdriver.PhantomJS(executable_path=selenium_path)

        log.info("Initialized. Selenium {}".format("installed. Path: {}".format(selenium_path) if webdriver else "not found, using minimal mode!"))


    # @handle_exceptions
    def get_user_by_name(self, username, selenium=True, allow_cache=True):
        """
        Gets a user profile by the username.
        :param username: string - username
        :param selenium: bool indicating if you want to use full browser Javascript support (making all features available but slowing it down)
        :param allow_cache: bool indicating if the cache is allowed to be used
        :return: User object or None if the user does not exist
        """
        if not self.selenium_available:
            selenium = False

        # Fetch from cache if allowed to
        if allow_cache and (str(username) in self.cache):
            if int(time.time()) - int(self.ages.get(str(username))) < self.max_age:
                assert isinstance(self.cache.get(str(username)), User)

                log.info("Using cache for {}".format(username))
                return self.cache.get(str(username))

            # Ignore cache if it's older than max_age
            else:
                pass

        # Use if selenium and phantomJS are installed and enabled
        # HIGHLY RECOMMENDED to install and use selenium
        if selenium:
            # a = webdriver.PhantomJS(executable_path=self.selenium_path)
            self.pjs.get(user_search + url_encode(username))
            u = self.pjs.page_source

            self.pjs.close()

        # Or just use urllib
        # WARNING! Not all functions are available when using this mode!
        else:
            log.info("Selenium not installed or disabled, using minimal mode")
            u = urlopen(user_search + url_encode(username))

        # BS Instance
        sp = BeautifulSoup(u, "html.parser")

        # Check if the user actually exists
        if clean(sp.find("div", {"class": "paddingboth"}).text).startswith("The user you are looking for was not found"):
            return None

        tm = time.time()
        try:
            username = clean(sp.find("div", {"class": "profile-username"}).text)
        except AttributeError:
            username = None

        try:
            age = clean(sp.find("div", {"title": "Age"}).text).strip(" years")
        except AttributeError:
            age = None

        try:
            occupation = clean(sp.find("div", {"title": "Occupation"}).text)
        except AttributeError:
            occupation = None

        try:
            interests = clean(sp.find("div", {"title": "Interests"}).text)
        except AttributeError:
            interests = None

        try:
            country = sp.find("img", {"class": "flag"}).get("title")
        except AttributeError:
            country = None

        # UTC time
        date_joined = sp.find("div", {"title": "Arrived"}).find("time", {"class": "timeago"}).text
        date_active = sp.find("div", {"title": "Last Active"}).find("time", {"class": "timeago"}).text

        if selenium:
            mid = clean(sp.find("div", {"class": "profileStatLine"}).find("b").text)
            rank_world = mid.strip("Performance: ").split("(")[0]
            rank_country = clean(sp.find("div", {"class": "profileStatLine"}).find("span").text)
            performance = mid.strip("Performance: ").split("(")[1].strip(")")

            # print(rank_world, rank_country, performance, sep="\n")

            pages = sp.find("div", {"id": "general"}).find_all("div", {"class": "profileStatLine"})
            pages.pop(0)

            ranked_score = clean(pages.pop(0).text.strip("Ranked Score")).strip(": ")
            hit_accuracy = clean(pages.pop(0).text.strip("Hit Accuracy")).strip(": ")
            play_count = clean(pages.pop(0).text.strip("Play Count")).strip(": ")
            play_time = clean(pages.pop(0).text.strip("Play Time")).strip(": ")
            total_score = clean(pages.pop(0).text.strip("Total Score")).strip(": ")
            level = clean(pages.pop(0).text.strip("Current Level")).strip(": ")
            total_hits = clean(pages.pop(0).text.strip("Total Hits")).strip(": ")
            max_combo = clean(pages.pop(0).text.strip("Maximum Combo")).strip(": ")

        else:
            # Assign all variables as None if selenium is not installed or disabled
            rank_world = rank_country = performance = ranked_score = hit_accuracy = None
            play_time = play_count = total_score = level = total_hits = max_combo = None

        # Generates an object
        obj = User(
            username=username,
            age=age,
            occupation=occupation,
            interests=interests,
            country=country,
            date_joined=date_joined,
            date_active=date_active,
            rank_world=rank_world,
            rank_country=rank_country,
            performance=performance,
            ranked_score=ranked_score,
            hit_accuracy=hit_accuracy,
            play_count=play_count,
            play_time=play_time,
            total_score=total_score,
            level=level,
            total_hits=total_hits,
            max_combo=max_combo
        )

        print("Creation took {}".format(time.time() - tm))

        self.cache[username] = obj
        self.ages[username] = int(time.time())
        return obj


# Tests
# logging.basicConfig(level=logging.INFO)
# o = OsuParser(selenium_path="phantomjs/phantomjs.exe")
# while True:
#     user = input("Name:")
#     t = time.time()
#     user = o.get_user_by_name(user, selenium=True)
#     print(user.username, user.max_combo)
#     print("Took {}".format(time.time() - t))
#
