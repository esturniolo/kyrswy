import urllib.request
import tweepy
import getpass
import twitter_secrets


def twitter(stream_radio_station, stream_show, twitter_username, will_you_grab_twitter_pic):
    upload = will_you_grab_twitter_pic

    if upload == "true":
        get_twitter_profile_pic(stream_radio_station,
                                stream_show, twitter_username)


def get_twitter_profile_pic(stream_radio_station, stream_show, twitter_username):
    consumer_key = twitter_secrets.twitter_consumer_key
    consumer_secret = twitter_secrets.twitter_consumer_secret
    access_key = twitter_secrets.twitter_access_key
    access_secret = twitter_secrets.twitter_access_secret
    host_username = getpass.getuser()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)

    user = api.get_user(screen_name=twitter_username)

    profile_image_url_https = user.profile_image_url_https

    profile_image_url_https = profile_image_url_https.replace(
        "_normal", "_400x400")

    urllib.request.urlretrieve(
        profile_image_url_https, f'/home/{host_username}/kyrswy/stations/{stream_radio_station}/{stream_show}/twitter_pic/' + twitter_username + '.png')
