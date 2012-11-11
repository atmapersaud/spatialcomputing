# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:06:58 2012

@author: mike
"""

from pyspatialite import dbapi2 as spatialdb
import numpy as np
from scipy.cluster.vq import vq as vq
from pysal.core.IOHandlers import wkt
wkt = wkt.WKTParser()

inDb = 'gooddbs/newdb2.db'
conn = spatialdb.Connection(inDb)
cur = conn.cursor()

countyCentroid = cur.execute('select intptlat10, intptlon10, geoid10 from countyfinal').fetchall()
print len(countyCentroid)
countyCentroid = [list((tuple((float(y),float(x))), id)) for x, y, id in countyCentroid]
countyArray = np.array(map(lambda x: x[0], countyCentroid))
countyDict = {count:id[1] for count, id in enumerate(countyCentroid)}

tweetPoints = cur.execute('select tweet_id, astext(coords) from status').fetchall()
print len(tweetPoints)
tweetPoints = [list((wkt(point), id)) for id, point in tweetPoints]
tweetArray = np.array(map(lambda x: x[0], tweetPoints))
tweetDict = {count:id[1] for count, id in enumerate(tweetPoints)}

closest = vq(tweetArray, countyArray)
myList = []
for count, countyindex in enumerate(closest[0]):
    county = countyDict[countyindex]
    twitter_id = tweetDict[count]
    myList.append((county, twitter_id))
    
cur.execute('create table countytweet (geoid10 text, tweet_id text)')
cur.executemany('insert into countytweet values(?,?)', myList)
    
conn.commit()
conn.close()
print True