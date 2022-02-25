import os
import sys
import glob
import datetime

sys.path.append('..')

from api_tasks.phishnet_api import PhishNetAPI

def get_images_diff():
    
    phishnetapi = PhishNetAPI()
    all_shows_list = phishnetapi.get_show_dates_list()
    
    current_shows_list = []
    current_shows_glob = glob.glob('../static/img/livephish_logos/*')
    for path in current_shows_glob:
        
        current_shows_list.append(os.path.basename(path).split('.')[0])
        
    missing_shows = set(all_shows_list) - set(current_shows_list)
    
    ordered_missing_shows = sorted(missing_shows, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    
    for missing_show in ordered_missing_shows:
        print(missing_show)
    
    return ordered_missing_shows
    
def main():
    get_images_diff()
    
if __name__ == '__main__':
    main()