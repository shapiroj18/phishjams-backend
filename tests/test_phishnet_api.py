import os
import sys

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from app import app
from app.api_tasks.phishnet_api import PhishNetAPI


def test_phishnet_root_endpoint():

    p = PhishNetAPI()
    assert p.get_root_endpoint().status_code == 200


def test_phishnet_get_all_jamcharts():

    p = PhishNetAPI()
    error_level = p.get_all_jamcharts()["error"]

    assert error_level == False


def test_phishnet_get_random_jam():
    p = PhishNetAPI()
    resp = p.get_random_jam()
    assert len(resp) == 3


def test_phishnet_get_random_jam_song(song="Back on the train"):
    p = PhishNetAPI()
    resp = p.get_random_jam()
    assert len(resp) == 3


def test_phishnet_get_random_jam_year(year="2019"):
    p = PhishNetAPI()
    resp = p.get_random_jam()
    assert len(resp) == 3


def test_phishnet_get_random_jam_song_year(song="Back on the train", year="2019"):
    p = PhishNetAPI()
    resp = p.get_random_jam()
    assert len(resp) == 3
