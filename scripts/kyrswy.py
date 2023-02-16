import os
import sys
import argparse
import configparser
import getpass
from create_dirs import create_dirs
from twitter_profile_grabber import twitter
from rec_stream import rec_stream
from rclone_uploader import rclone_upload_log_file, rclone_upload_mp3_file
from mixcloud_uploader import mixcloud
from delete_old_files import delete_old_files


def read_config(config_file):
    config_file = os.path.abspath(config_file)
    config = configparser.ConfigParser()
    config.read(config_file)

    stream_url = config["DEFAULT"]["stream_url"]
    stream_radio_station = config["DEFAULT"]["radio"]
    stream_show = config["DEFAULT"]["show"]

    will_you_grab_twitter_pic = config["DEFAULT"]["will_you_grab_twitter_pic"]
    twitter_username = config["DEFAULT"]["twitter_username"]

    rclone_cloud_name = config["DEFAULT"]["rclone_name"]
    rclone_logs_cloud_name = config["DEFAULT"]["rclone_logs_name"]

    will_be_uploaded_to_mixcloud = config["DEFAULT"]["will_be_uploaded_to_mixcloud"]
    mixcloud_tag0 = config["DEFAULT"]["mixcloud_tag0"]
    mixcloud_tag1 = config["DEFAULT"]["mixcloud_tag1"]
    mixcloud_tag2 = config["DEFAULT"]["mixcloud_tag2"]
    mixcloud_tag3 = config["DEFAULT"]["mixcloud_tag3"]
    mixcloud_tag4 = config["DEFAULT"]["mixcloud_tag4"]

    rec_time_minutes = int(config["DEFAULT"]["rec_time_minutes"])

    return stream_url, rec_time_minutes, stream_radio_station, stream_show, will_you_grab_twitter_pic, twitter_username, rclone_cloud_name, rclone_logs_cloud_name, will_be_uploaded_to_mixcloud, mixcloud_tag0, mixcloud_tag1, mixcloud_tag2, mixcloud_tag3, mixcloud_tag4


if __name__ == "__main__":
    user = getpass.getuser()

    if len(sys.argv) != 2:
        print(
            f"Usage: python3 /home/{user}/kyrswy/scripts/kyrswy.py /home/{user}/kyrswy/shows/[config_file.ini]")
        sys.exit(1)
    config_file = sys.argv[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file",
                        help="Config file name.")
    args = parser.parse_args()

    stream_url, rec_time_minutes, stream_radio_station, stream_show, will_you_grab_twitter_pic, twitter_username, rclone_cloud_name, rclone_logs_cloud_name, will_be_uploaded_to_mixcloud, mixcloud_tag0, mixcloud_tag1, mixcloud_tag2, mixcloud_tag3, mixcloud_tag4 = read_config(
        args.config_file)

    create_dirs(stream_radio_station, stream_show)
    twitter(stream_radio_station, stream_show,
            twitter_username, will_you_grab_twitter_pic)
    rec_stream(stream_url, rec_time_minutes,
               stream_radio_station, stream_show, will_you_grab_twitter_pic, twitter_username)
    rclone_upload_mp3_file(stream_radio_station,
                           stream_show, rclone_cloud_name, rec_time_minutes)
    rclone_upload_log_file(stream_radio_station,
                           stream_show, rclone_logs_cloud_name)
    mixcloud(stream_radio_station, stream_show, twitter_username, mixcloud_tag0, mixcloud_tag1,
             mixcloud_tag2, mixcloud_tag3, mixcloud_tag4, will_be_uploaded_to_mixcloud)
    delete_old_files(stream_radio_station, stream_show)
