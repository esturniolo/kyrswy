import subprocess
import getpass

host_username = getpass.getuser()


def delete_old_files(stream_radio_station, stream_show):
    host_directory = f"/home/{host_username}/kyrswy/stations/{stream_radio_station}/{stream_show}"
    subprocess.run(["find", f"{host_directory}/recordings", "-type",
                   "f", "-mtime", "+5", "-iname", "*.mp3", "-delete"])
