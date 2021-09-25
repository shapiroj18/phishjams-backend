import os
import sys

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from app import app
from app.api_tasks.phishin_api import PhishINAPI

def test_get_show_on_date():
    p = PhishINAPI()
    resp = p.get_show_on_date('2021-08-27')
    
    assert resp['success'] == True
    
def test_get_song_url():
    p = PhishINAPI()
    resp = p.get_song_url('camel walk', '2021-08-27')
    
    assert resp == 'https://phish.in/audio/000/034/980/34980.mp3'