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
        phishnet_endpoint = "https://api.phish.net/v5/"

        with httpx.Client() as client:
            payload = {"apikey": api_key}
            response = client.get(url=phishnet_endpoint, params=payload)

            return response

    def get_all_jamcharts(self):
        phishnet_endpoint = "https://api.phish.net/v5/jamcharts/"

        with httpx.Client() as client:

            payload = {
                "apikey": api_key,
            }

            response = client.get(url=phishnet_endpoint, params=payload)

            return response.json()

    def get_random_jam(self, song=None, year=None):

        jamcharts = self.get_all_jamcharts()["data"]

        entries_to_randomize = []

        if song and year:
            for entry in jamcharts:
                if entry["song"].lower() == song.lower() and entry["showyear"] == year:
                    entries_to_randomize.append(entry)

        elif song:
            for entry in jamcharts:
                if entry["song"].lower() == song.lower():
                    entries_to_randomize.append(entry)

        elif year:
            for entry in jamcharts:
                if entry["showyear"] == year:
                    entries_to_randomize.append(entry)

        else:
            for entry in jamcharts:
                entries_to_randomize.append(entry)

        random_entry = random.choice(entries_to_randomize)

        song = random_entry["song"]
        date = random_entry["showdate"]
        show_info = random_entry["permalink"]

        return song, date, show_info
    
    def get_specific_jam(self, song, date):
        
        jams = []

        jamcharts = self.get_all_jamcharts()["data"]
        for entry in jamcharts:
            if entry["song"].lower() == song.lower() and entry['showdate'] == date:
                jams.append(entry)
                
        if len(jams) != 1:
            raise ValueError('More than one jam found')
        else:
            show_info = jams[0]['permalink']
            return song, date, show_info
        
    def get_show_dates_list(self):
        phishnet_endpoint = "https://api.phish.net/v5/shows"

        with httpx.Client() as client:
            payload = {"apikey": api_key}
            response = client.get(url=phishnet_endpoint, params=payload)
            
            all_shows_list = []
            for show in response.json()['data']:
                if show['artistid'] == '1':
                    all_shows_list.append(show['showdate'])
                

            return all_shows_list