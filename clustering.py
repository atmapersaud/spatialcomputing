# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 19:10:39 2012

@author: mike
"""
# here we do some importing
from pyspatialite import dbapi2 as spatialdb
import numpy as np
from scipy.cluster.vq import kmeans as kmeans
from pylab import show, plot

from collections import defaultdict
from pysal.core.IOHandlers import wkt
import pysal
wkt = wkt.WKTParser()
    

inDb = 'newdb.db'
conn = spatialdb.Connection(inDb)
cur = conn.cursor()

# simple queries to get some information out of the database
wordsQuery = """select distinct(word) from words"""
                        
hashesQuery = """select distinct(hash) from hash_tweet
                        group by hash
                        having count(*) > 10;"""
                        
selectCoords = """select astext(transform(status.coords, 5070))
    from status join words 
    on status.tweet_id = words.tweet_id
    where words.word = ?"""

hashDict = {}
for hashtag in cur.execute(hashesQuery).fetchall():
    print hashtag
    points = []
    for point in cur.execute(selectCoords, hashtag).fetchall():
        points.append(wkt(point[0]))
    hashDict[hashtag[0]] = np.array(points)
    
# a little idea
        

obama = hashDict['Obama']
romney = hashDict['Romney']
b = kmeans(romney, 5)
b_x = [x[0] for x in b[0]]
b_y = [x[1] for x in b[0]]
romney_x = [x[0] for x in romney]
romney_y = [x[1] for x in romney]
a = kmeans(obama, 5)
a_x = [x[0] for x in a[0]]
a_y = [x[1] for x in a[0]]
pl = plot(a_x, a_y, 'kd')
pl = plot(b_x, b_y, 'yd')

obama_x = [x[0] for x in obama]
obama_y = [x[1] for x in obama]
plot(obama_x, obama_y, 'bd')
plot(romney_x, romney_y,'rd')
show()
        
                            