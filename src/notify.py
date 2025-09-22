import os
from pushbullet import Pushbullet

def send_error_notification(message):
    PB_API_KEY = os.getenv('PUSHBULLET_API_KEY')
    pb = Pushbullet(PB_API_KEY)
    push = pb.push_note("UHC API Input Generator Error", f"{message}")