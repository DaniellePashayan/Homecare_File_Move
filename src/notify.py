import os
from pushbullet import Pushbullet

def send_error_notification(message):
    API_KEYS = []
    API_KEYS.append(os.getenv('PUSHBULLET_API_KEY'))
    API_KEYS.append(os.getenv('PUSHBULLET_API_KEY_DAVID'))
   
    for api_key in API_KEYS:
        if api_key:
            pb = Pushbullet(api_key)
            pb.push_note("ERROR: Homecare File Move", f"{message}")