import getpass
import os


def create_dirs(stream_radio_station, stream_show):
    user = getpass.getuser()

    full_path = f"/home/{user}/kyrswy/stations/{stream_radio_station}/{stream_show}"

    rec_path = (
        f"{full_path}/recordings")
    os.makedirs(rec_path, exist_ok=True)

    twitter_pic_path = (
        f"{full_path}/twitter_pic")
    os.makedirs(twitter_pic_path, exist_ok=True)

    logs_path = (
        f"{full_path}/logs")
    os.makedirs(logs_path, exist_ok=True)
