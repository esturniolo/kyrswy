# KYRSWY (Keep Your Radio Show With You)

KYRSWY is a radio recorder done in Python that uses [Rclone](https://rclone.org/) to upload your final recording to any cloud service that Rclone supports.

I've been using this for years. First with an ugly bash script and then in Python.

To be totally honest, sometimes I forgot that is working because is very robust and when it fails, it's something related to the Radio Station and not for the script. 

It was tested on Alpine Linux 3.16 and Ubuntu 22.04, but it should work in almost any distro that has Python 3.x, Rclone, pip and Docker installed.

It should work too in any ARM based hardware (i.e. Rapsberry Pi), the only difference should be [use an ARM ffpmeg docker image like the LinuxServer.io one](https://github.com/linuxserver/docker-ffmpeg).

The Rclone part was tested with the following cloud services:
- Google Drive
- Dropbox
- Box
- WebDav
And should work with all the cloud services that Rclone provides.

# Requirements
- Linux system
- Python3
- Docker
- Rclone
- Pip
- The libraries listed on the `requirements.txt` file.


# How does it work and how does it do it?
You have two main scripts in `./kyrswy/scripts` directory:
- cron.py → Script who call the `kyrswy.py` script to rec the streaming.
- kyrswy.py → Script who finally rec all the streaming. This script uses the [jrottenberg ffmpeg Docker container](https://github.com/jrottenberg/ffmpeg) to rec the streaming that you add in the `.ini` file.

And the show files are in `./kyrswy/shows`. In this repo you have one `ini` file as an example. 
Inside that file you must add the following info:
- `stream_url` → This is the most important item into the file. And here you need to put the stream to rec.
- `radio` → Radio station name (please don't use spaces in this field)
- `show` → Radio show name (same advice as before)
- `rec_time_minutes` → How many minutes you will rec the show.
- `rclone_name` → The name of the remote that you used to configure your cloud service.
- `rclone_logs_name` → The same as before in case that you want use the same remote. If you want to use another cloud service to keep your logs (as me), just put the name of the other remote.
- `will_be_uploaded_to_mixcloud` → This is just a boolean option "Will be uploaded to Mixcloud? True or False"
- `mixcloud_tag[x]` → different tags to add in Mixcloud service. Max are 5 starting from 0 (0 to 4)
- `cron_hour` → The values that you use in your usual crontab file. Including `/` `*` `-`
- `cron_minute` → idem
- `cron_day_month` idem 
- `cron_month` → idem
- `cron_day_week` → idem

All the magic (?) was thinked to use only the `cron.py` file combined with the `.ini` file.
The idea is that you can have different `.ini` files: one for every Radio Show that you want to record. 
Once you ran the `cron.py` with the `.ini` file (`$ python3 ~/kyrswy/scripts/cron.py ~/kyrswy/shows/[name_of_file.ini]`), automagically a new entry should be appear in your `crontab` file who will wait until the exact time that you set in the `.ini` file to start to rec.

You can use `kyrswy.py` script alone too to start manually your recording combined with the `.ini` file: `$ python3 ~/kyrswy/scripts/kyrswy.py ~/kyrswy/shows/[name_of_file.ini]`

After the rec ends, the script will call the Rclone remote to upload the mp3 file and logs. Locally you can find the files in `~/kyrswy/stations/[name_of_the_radio_station]/[name_of_the_radio_show]/recordings` and logs `~/kyrswy/stations/[name_of_the_radio_station]/[name_of_the_radio_show]/logs`. The logs will overwrite everytime you made a new record.

The file will be named as `YYYY-MM-DD-[name_of_the_radio_station]-[name_of_the_radio_show].mp3`. So if you run the script twice in the day, you will overwrite the previuos recording. This was made because a Radio Show will be on air only one time a day.

The script will delete the old files to keep always the last 5 of them deleting the old one only in the host, keeping all the recordings safe in the cloud service.

## TL;DR
- Clone this repo into your home directory (yes, is intended to work from `~/kyrswy`).
- Create all the `.ini` files that you want or need following the instructions mentioned above.
- Execute the script `$ python3 ~/kyrswy/scripts/cron.py ~/kyrswy/shows/[name_of_file.ini]` 
- Take some coffee and wait to get your audio file ready in you cloud service that you configured before with Rclone.
- Enojy listen them whenever you want.

---
# Setup
- Install Docker. You can do it following [this very well explained official guide](https://docs.docker.com/engine/install/ubuntu/)
- Install Rclone. you have several option to do it. You can find all the ways in the [Rclone Offical install guide](https://rclone.org/install/)
- Install Python3 and pip (but c'mon... if you reached this point I think that you already have this installed)
- Install the pip libraries needed: `$ pip install -r requirements.txt`

## Secrets
### Telegram
The only secrets file that you must fill is the Telegram one to get all the notifications.

_Why you say that? I don't need notifications!_

Believe me you little Padawan, you will.

Talking from my own experience, sometimes the connection between ffmpeg and the streaming link fails and that it's 99.999999% for the Radio Stations reasons...
- Some error 5xx.
- Some 404 because the changed the link. 
- Some error because they reached the maximun listeners.
- And a lot of etc...

So if you face some of this situations and you don't have notifications about this, you'll be very dissapointed when you realize that your special show is not recorded.

So if you don't have one, create a Telegram account, [create a bot with BotFather](https://core.telegram.org/bots#how-do-i-create-a-bot) and be happy.

To get your own `chat_id` I found a very simple solution using a [RawDataBot](https://botostore.com/c/rawdatabot/). After you start a chat with that bot, it will return to you all the data of that chat including your `chat_id`.

Seems to be totally harmless, **but use it at your own risk**

### Twitter
You can let the `twitter_secrets.py` as it is if you don't want to download the profile pic of your Radio Show.
For this, just leave as `false` the option `will_you_grab_twitter_pic` in your `.ini` file.

If you want to get the pic profile, you need to create a free Twitter App using the [Developer Portal](https://developer.twitter.com) as long as Elon wants :)

### Mixcloud
Same as Twitter. If you don't want to upload you show to Mixcloud, just leave the `will_be_uploaded_to_mixcloud` as `false`
To get an API key you will need to [create a new application on Mixcloud Developer website](https://www.mixcloud.com/developers/)


# Final words
I'm not a Python programmer. I created this just for fun. 

The code could be better? Yes

The code could be shorter? Yes

The code could be more simple? Yes

The code has some bugs? I hope not...

But works, is robust, easy to use and does what it says, so...

Happy recordings!

---
# DISCLAIMER
All the content that you can record is property of their own Radio Transmitter, Radio Host, Radio Show, Radio Station and/or all the people/enterprises involved in the transmission.

This was made only for educational purposes.