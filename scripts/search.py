import parsetest
from basicTwitter import auth
import tweepy

print dir (parsetest)
api = auth()
print dir(api)


#for status in tweepy.Cursor(api.friends_timeline).items(200):
 #   # Process the status here
  #  print status.text

def getFollowers(user):
    return user.followers()

def getFriends(user):
    return user.friends()

def getTimeline(api, user):
    return api.user_timeline(user)

print getFollowers(api.me())
# print getFriends(api.me())
print dir(getTimeline(api, api.me())[1])

print dir(tweepy.Cursor(api.followers))

for friend in tweepy.Cursor(api.followers).iterator:
    print [x.text for x in getTimeline(api, friend)]
