import configparser
import getpass
import subprocess
import sys
import re
import os

arg = sys.argv[1]
remove = False
if arg == '-r':
    remove = True
    arg = sys.argv[2]

host_username = getpass.getuser()

config = configparser.ConfigParser()
config.read(arg)

minute = config["DEFAULT"]["cron_minute"]
hour = config["DEFAULT"]["cron_hour"]
day_of_month = config["DEFAULT"]["cron_day_month"]
month = config["DEFAULT"]["cron_month"]
day_of_week = config["DEFAULT"]["cron_day_week"]
script_path = f"/home/{host_username}/kyrswy/scripts/kyrswy.py"
config_path = arg

crontab_entry = f"{minute} {hour} {day_of_month} {month} {day_of_week} python3 {script_path} {config_path}"

crontab_output = subprocess.run(
    ['crontab', '-l'], capture_output=True, text=True).stdout

if not crontab_output:
    crontab_output = ""

entry_pattern = re.escape(crontab_entry.replace("+", "\\+"))

if not re.search(fr'^{entry_pattern}$', crontab_output, flags=re.MULTILINE):
    if not remove:
        with open('/tmp/crontab_entry.txt', 'w') as file:
            file.write(crontab_output + crontab_entry + "\n\n")
        subprocess.run(['crontab', '/tmp/crontab_entry.txt'])
        print("\nThe show was added to crontab file.\n")
    else:
        print("\nThis show does not exist in crontab.\n")
else:
    if remove:
        with open('/tmp/crontab_entry.txt', 'w') as file:
            file.write(re.sub(fr'^{entry_pattern}$', '',
                       crontab_output, flags=re.MULTILINE))
        subprocess.run(['crontab', '/tmp/crontab_entry.txt'])
        print("\nThe show was removed from the crontab file.\n")
    else:
        print("\nThis show already exists in crontab.\n")

if os.path.exists('/tmp/crontab_entry.txt'):
    subprocess.run(['rm', '/tmp/crontab_entry.txt'])
