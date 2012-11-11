# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:06:58 2012

@author: mike
"""
# import all of modules
from pyspatialite import dbapi2 as spatialdb
import numpy as np
from scipy.cluster.vq import vq as vq
from pysal.core.IOHandlers import wkt

# this is how we start the wkt parser
wkt = wkt.WKTParser()

# set up a cursor
inDb = 'gooddbs/newdb2.db'
conn = spatialdb.Connection(inDb)
cur = conn.cursor()

# grab all of the countyCentroids
countyCentroid = cur.execute(
                """select intptlat10, intptlon10, geoid10
                from countyfinal""").fetchall()
# alittle formatting
countyCentroid = [list((tuple((float(y),float(x))), id)) 
                    for x, y, id in countyCentroid]
# turn into an array of points
countyArray = np.array(map(lambda x: x[0], countyCentroid))
# a dictionary of position in list to id
countyDict = {count:id[1] for count, id in enumerate(countyCentroid)}

# same process for the status points
tweetPoints = cur.execute("""select tweet_id, astext(coords) 
                    from status""").fetchall()
tweetPoints = [list((wkt(point), id)) for id, point in tweetPoints]
tweetArray = np.array(map(lambda x: x[0], tweetPoints))
tweetDict = {count:id[1] for count, id in enumerate(tweetPoints)}

# find the closest county for each tweet
closest = vq(tweetArray, countyArray)
# create a blank list
myList = []
# loop through each of the matches
for count, countyindex in enumerate(closest[0]):
    # the number in there is the index so grab it from the dictionary of counties
    county = countyDict[countyindex]
    # and we do the same here
    twitter_id = tweetDict[count]
    # and append it onto a list
    myList.append((county, twitter_id))

# create our table
cur.execute("""create table if not exists countytweet (
                geoid10 text, tweet_id text)""")
# and put in all of the shit
cur.executemany('insert into countytweet values(?,?)', myList)
# finish the transaction and close it   
conn.commit()
conn.close()
# let the user know that it is done
print True