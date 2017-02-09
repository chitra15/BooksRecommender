from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy

access_token= "4204466597-rHw64J65sdQdrkThqYoxIU4pEOgTU2kl9pCJsXb"
access_token_secret= "TwwMFZCqvCoYOGOm3LQbLnmJ4qBQMbGgplXcExB9o6ElB"
consumer_key= "SBsZKzoy7YgfeuVonSg4zq5XU"
consumer_secret= "kLxNsuuRh4RPxn5sM9blj3k6dGbq5krck0XjMDjkc3fduIWti2"

class StreamListener(StreamListener):

    def on_data(self, data):
        print (data)
        return

    def on_error(self, status):
        print(status)

if __name__== '__main__':

    str=StreamListener()
    auth= OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api= tweepy.API(auth)

    stream= Stream(auth=api.auth, listener=str)

    stream.filter(follow=['575930104'])

