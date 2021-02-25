import os
import json
import random
import requests
import httpx
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

api_key = os.getenv("PHISHNET_API_KEY")


class PhishNetAPI:
    def __init__(self):
        self.api_key = api_key

    def get_root_endpoint(self):
        phishnet_endpoint = "https://api.phish.net/v3/"

        with httpx.Client() as client:
            payload = {"apikey": api_key}
            response = client.get(url=phishnet_endpoint, params=payload)

            return response

    def get_all_jamcharts(self):
        phishnet_endpoint = "https://api.phish.net/v3/jamcharts/all"

        with httpx.Client() as client:

            payload = {
                "apikey": api_key,
            }

            response = client.get(url=phishnet_endpoint, params=payload)

            return response.json()

    def get_one_jamchart(self, songid):
        phishnet_endpoint = "https://api.phish.net/v3/jamcharts/get"

        with httpx.Client() as client:
            payload = {"apikey": api_key, "songid": songid}

            response = client.get(url=phishnet_endpoint, params=payload)

            return response.json()
        
        

    def get_jamchart_song_ids(self, song=None):
        response = self.get_all_jamcharts()

        if song:
            for item in response["response"]["data"]:
                if item["song"].lower() == song.lower():
                    song_ids = [item["songid"],]
        else:
            song_ids = []
            for item in response["response"]["data"]:
                song_ids.append(item["songid"])

        return song_ids

    def get_random_jamchart(self, song=None):
        jamchart_song_ids = self.get_jamchart_song_ids(song)
        
        song_id = random.choice(jamchart_song_ids)
        chart = self.get_one_jamchart(song_id)
        song = chart["response"]["data"]["song"]
        
        entries_count = len(chart["response"]["data"]["entries"])
        date = chart["response"]["data"]["entries"][
            random.randrange(entries_count)
        ]["showdate"]

        return song, date

    def get_show_url(self, date):
        # handle nonexistant lookups
        phishnet_endpoint = "https://api.phish.net/v3//setlists/get"

        with httpx.Client() as client:

            payload = {"apikey": api_key, "showdate": date}

            response = client.get(url=phishnet_endpoint, params=payload)

            return response.json()["response"]["data"][0]["url"]
