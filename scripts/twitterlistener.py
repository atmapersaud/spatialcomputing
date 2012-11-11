from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys, json, shelve
import parsetest
from pyspatialite import dbapi2 as spatialdb



## security shit (change to your own)
consumer_key = '1nrA8Nqe4awDmy5c4D5fg'
consumer_secret = 'WvtbdEYvcuXiNGhBVa4TOjiLwTEF5Xra0FrEdgA'
access_token = '183620373-VxCczsD8En3OH8K0s8OebXRFPd7MS54Npr1JZaJ6'
access_token_secret = 'psP1iNbGhxqH8aFD1TKvEcHzmLPWi6Inp9g6i81LoA'

# this is to make it so i dont need to look it up because i forget the syntax
def runSql(inDb, sqlCommand, params):
    """takes sql command and executes it in a transaction. read sqlite3 documentation """
    conn = sqlite3.Connection(inDb)
    cur = conn.cursor()
    cur.execute(sqlCommand, params)
    conn.commit()
    conn.close()

# found this in the tweepy examples and changed it slightly to dump straight to db
class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, conn=None,cur=None):
        self.conn = conn
        self.cur = cur
        
    def on_data(self, data):
        try:
            data = json.loads(r'{0}'.format(data))
            parsetest.run(data,self.cur, self.conn)
        except Exception as e:
            print 'error here', e,
        finally:
            self.conn.commit()

    def on_error(self, status):
        print 'error', status


if __name__ == '__main__':
    try:
        # in database name
        inDb = sys.argv[1]
        # terms to look for
        keywords = sys.argv[2:] # example ['obama','romney','ryan','biden','independent','republican','democrat']
        #open a shelve (stupid python key value store)
        conn = spatialdb.Connection(inDb)
        cur = conn.cursor()
        l = StdOutListener(conn, cur)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)
        stream.filter(track=keywords, locations =[-124,24,-66,49])#united states bbox
    finally:
        if conn: conn.close()

