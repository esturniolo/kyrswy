import requests
import getpass
import time
import mixcloud_secrets


def mixcloud(stream_radio_station, stream_show, twitter_username, mixcloud_tag0, mixcloud_tag1, mixcloud_tag2, mixcloud_tag3, mixcloud_tag4, will_be_uploaded_to_mixcloud):
    upload = will_be_uploaded_to_mixcloud

    if upload == "true":
        upload_to_mixcloud(stream_radio_station, stream_show, twitter_username,
                           mixcloud_tag0, mixcloud_tag1, mixcloud_tag2, mixcloud_tag3, mixcloud_tag4)


def upload_to_mixcloud(stream_radio_station, stream_show, twitter_username, mixcloud_tag0, mixcloud_tag1, mixcloud_tag2, mixcloud_tag3, mixcloud_tag4):
    mixcloud_secret = mixcloud_secrets.mixcloud_secret
    timestamp = time.strftime("%Y-%m-%d")
    host_username = getpass.getuser()
    host_directory = f"/home/{host_username}/kyrswy/stations/{stream_radio_station}/{stream_show}"
    output_mp3_file = f"{host_directory}/recordings/{timestamp}-{stream_radio_station}-{stream_show}.mp3"
    twitter_pic = f"{host_directory}/twitter_pic/{twitter_username}.png"
    finalname = f"{stream_radio_station} - {stream_show} - {timestamp}"

    params = {
        'access_token': mixcloud_secret,
    }

    files = {
        'mp3': open(output_mp3_file, 'rb'),
        'name': (None, finalname),
        'picture': open(twitter_pic, 'rb'),
        'tags-0-tag': (None, f'{mixcloud_tag0}'),
        'tags-1-tag': (None, f'{mixcloud_tag1}'),
        'tags-2-tag': (None, f'{mixcloud_tag2}'),
        'tags-3-tag': (None, f'{mixcloud_tag3}'),
        'tags-4-tag': (None, f'{mixcloud_tag4}'),
        'description': (None, f'Show on air on {timestamp}'),
    }

    response = requests.post(
        'https://api.mixcloud.com/upload/', params=params, files=files)
