import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys, json, shelve
import sqlite3

    
# set this bullshit
def auth():
    consumer_key = '1nrA8Nqe4awDmy5c4D5fg'
    consumer_secret = 'WvtbdEYvcuXiNGhBVa4TOjiLwTEF5Xra0FrEdgA'
    access_token = '183620373-VxCczsD8En3OH8K0s8OebXRFPd7MS54Npr1JZaJ6'
    access_token_secret = 'psP1iNbGhxqH8aFD1TKvEcHzmLPWi6Inp9g6i81LoA'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api
    

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, db=None):
        self.db = db
        
    def on_data(self, data):
        try:
            data = json.loads(r'{0}'.format(data))
            self.db[str(data['id'])] = data
            self.db.sync()
            # a = Struct(data)
            # self.inlist.append(a)
            # for i in dir(a): print i, '\t', getattr(a,i)
            return True
        except Exception as e:
            print 'error here', e, data

    def on_error(self, status):
        print 'error', status