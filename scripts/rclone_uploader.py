import subprocess
import os
import getpass
import time
from telegram_sender import send_telegram_alert


def rclone_upload_mp3_file(stream_radio_station, stream_show, rclone_cloud_name, rec_time_minutes):
    timestamp = time.strftime("%Y-%m-%d")
    host_username = getpass.getuser()
    mp3_file = f"{timestamp}-{stream_radio_station}-{stream_show}.mp3"
    mp3_file_dir = f"/home/{host_username}/kyrswy/stations/{stream_radio_station}/{stream_show}/recordings"
    rclone_log_file = f"{timestamp}-{stream_radio_station}-{stream_show}-rclone.log"
    log_file_dir = f"/home/{host_username}/kyrswy/stations/{stream_radio_station}/{stream_show}/logs"
    destination = f"{rclone_cloud_name}:/kyrswy/{stream_radio_station}/{stream_show}/recordings"
    run_rclone_upload_mp3 = f"rclone copy {os.path.join(mp3_file_dir, mp3_file)} {destination} --log-level INFO --log-file={log_file_dir}/{rclone_log_file}"

    try:
        subprocess.run(run_rclone_upload_mp3.split(), check=True)
    except subprocess.CalledProcessError:
        minutes_to_wait = 10
        total_time_wait = rec_time_minutes + minutes_to_wait
        time_wait = total_time_wait * 60
        message = f"⚠️ WARNING ⚠️ \n\nFor some reason the file '{mp3_file}' of show '{stream_show}' doesn't upload to {rclone_cloud_name} 🤷🏻‍♂️.\nThe system will wait {minutes_to_wait} minutes to try to upload it again.\n\nI will keep you posted."
        send_telegram_alert(message)
        time.sleep(time_wait)
        try:
            message_retry = f"✅ Everything it's ok ✅\n\nAfter the retry it seems that '{mp3_file}' upload works.\n\nThat was close 😮‍💨."
            subprocess.run(run_rclone_upload_mp3.split(), check=True)
            send_telegram_alert(message_retry)
        except subprocess.CalledProcessError:
            message_error = f"🔴 ALERT 🔴\n\nAfter waiting {minutes_to_wait} minutes since the second try, the file '{mp3_file}' doesn't upload to '{rclone_cloud_name}' 😱.\n\nYou need to check this manually to see what happened 🚧 👷🏽 🚧.\n\nSorry."
            send_telegram_alert(message_error)


def rclone_upload_log_file(stream_radio_station, stream_show, rclone_logs_cloud_name):
    host_username = getpass.getuser()
    log_file_dir = f"/home/{host_username}/kyrswy/stations/{stream_radio_station}/{stream_show}/logs"
    destination = f"{rclone_logs_cloud_name}:/kyrswy/{stream_radio_station}/{stream_show}/logs"
    run_rclone_upload_logs = f"rclone copy {log_file_dir} {destination}"

    try:
        subprocess.run(run_rclone_upload_logs.split(), check=True)
    except subprocess.CalledProcessError:
        message = f"⚠️ WARNING ⚠️ \n\nFor some reason the logs of show '{stream_show}' doesn't upload to {rclone_logs_cloud_name} 🤷🏻‍♂️.\nIf you need them, you can find it in your server."
        send_telegram_alert(message)
