import os
import getpass
import socket
import subprocess
import time
from telegram_sender import send_telegram_alert


def rec_stream(stream_url, rec_time_minutes, stream_radio_station, stream_show, will_you_grab_twitter_pic, twitter_username):
    duration = rec_time_minutes * 60
    timestamp = time.strftime("%Y-%m-%d")
    host_username = getpass.getuser()
    host_directory = f"/home/{host_username}/kyrswy/stations/{stream_radio_station}/{stream_show}"
    userid = os.getuid()
    groupid = os.getgid()
    output_mp3_file = f"{timestamp}-{stream_radio_station}-{stream_show}.mp3"
    log_file = f"{host_directory}/logs/{timestamp}-{stream_radio_station}-{stream_show}-ffmpeg.log"
    rec_dir = f'{host_directory}/recordings'
    twitter_pic_dir = f'{host_directory}/twitter_pic'
    start_time = time.time()

    if will_you_grab_twitter_pic == "true":
        docker_run_command = f"docker run --rm --name {stream_radio_station}__{stream_show} -v {rec_dir}:/output/recordings -v {twitter_pic_dir}:/output/twitter_pic -u {userid}:{groupid} jrottenberg/ffmpeg -y -thread_queue_size 2048 -i {stream_url} -i /output/twitter_pic/{twitter_username}.png -map 0 -map 1:0 -t {duration} -c:a libmp3lame -metadata title={stream_show} -metadata artist={stream_radio_station} -c:a libmp3lame /output/recordings/{output_mp3_file} > {log_file} 2>&1"
    else:
        docker_run_command = f"docker run --rm --name {stream_radio_station}__{stream_show} -v {rec_dir}:/output/recordings -v {twitter_pic_dir}:/output/twitter_pic -u {userid}:{groupid} jrottenberg/ffmpeg -y -thread_queue_size 2048 -i {stream_url} -t {duration} -c:a libmp3lame -metadata title={stream_show} -metadata artist={stream_radio_station} -c:a libmp3lame /output/recordings/{output_mp3_file} > {log_file} 2>&1"

    try:
        subprocess.run(docker_run_command, shell=True, check=True)
    except Exception as err:
        hostname = socket.gethostname()
        elapsed_time = time.time() - start_time
        error = f"Recording error on host {hostname}:\n\n{err}\n\n\nTotal rec time {elapsed_time} minutes."
        send_telegram_alert(error)
        return
