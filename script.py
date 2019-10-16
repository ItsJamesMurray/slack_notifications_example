from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import json
import requests

client_key = "MY_CLIENT_KEY"
client_secret = "MY_CLIENT_SECRET"

token = "MY_TOKEN"
token_secret = "MY_TOKEN_SECRET"

# Send Notification to your Slack Channel
def notify_slack(text, tweet_id, screen_name, user_icon):
    url = "MY_SLACK_WEBHOOK_URL"
    payload = {"attachments": [{"fallback": screen_name + " says... " + text + ".\n  View this tweet at: https://twitter.com/i/web/status/{}".format(tweet_id),"color": "#36a64f","pretext": screen_name + " just tweeted:","author_name": screen_name,"author_icon": user_icon,"title": "Twitter","title_link": "https://twitter.com/i/web/status/{}".format(tweet_id),"text": text}]}
    print(payload)
    r = requests.post(url, data=json.dumps(payload))
    print(r.text)

class TweetListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        user_info = tweet['user']
        # Send tweet text & link to each tweet in Slack
        if(user_info['id_str'] in ["20950232", "16403943"]):
            notify_slack(tweet['text'], tweet['id'], user_info['screen_name'], user_info['profile_image_url_https'])
            print(tweet)
            return True

    def on_error(self, status_code):
        if(status_code == 420):
            # returning False in on_error disconnects the stream
            print("Error: %s" % status_code)
            return False


listener = TweetListener()
auth = OAuthHandler(client_key, client_secret)
auth.set_access_token(token, token_secret)
stream = Stream(auth, listener)

stream.filter(follow=["20950232", "16403943"], is_async=True)
