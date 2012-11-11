
/*find the mean location of a word not exactly right but still kinda close*/
select sum(x(status.coords))/count(status.tweet_id), sum(y(status.coords))/count(status.tweet_id), words.word
	from words inner join status on status.tweet_id = words.tweet_id
	group by word
	having count(*) > 10
	order by count(*) desc;

/*this would find the mean location of hash tags*/
select sum(x(status.coords))/count(status.tweet_id), sum(y(status.coords))/count(status.tweet_id), hash_tweet.hash, count(*)
	from hash_tweet inner join status on hash_tweet.tweet_id = status.tweet_id
	group by hash_tweet.hash
	having count(*) > 10
	order by count(*) asc;

/*now lets find words that are far away from the mean location of tweets */
select sum(x(status.coords))/count(status.tweet_id), sum(y(status.coords))/count(status.tweet_id)
	from status;

/*create a simple table for romney and obama*/
create table romney as 
	select * from status 
	where status.tweet_id in 
		(select tweet_id from hash_tweet 
			where upper(hash) like '%ROMNEY%');

SELECT RecoverGeometryColumn('romney', 'coords', 4326, 'POINT', 'XY');
SELECT CreateSpatialIndex('romney', 'coords');

create table obama as 
	select * from status 
	where status.tweet_id in 
	(select tweet_id from hash_tweet 
	where upper(hash) like '%OBAMA%');
SELECT RecoverGeometryColumn('obama', 'coords', 4326, 'POINT', 'XY');
SELECT CreateSpatialIndex('obama', 'coords');

/*this is the command to load a census shape file into the geodatabase*/
/*clearly takes an unzipped shapefile*/
 .loadshp countyshp/tl_2010_us_county10 county2 ISO-8859-1 4269
/*not sure if it gets a pre made spatial index??*/
SELECT CreateSpatialIndex('county2', 'geometry');


/*and now to aggregate by county*/
/*first add some columns to the county*/
begin;
alter table county2
add column totaltweets integer;
alter table county2
add column romneyCount integer;
alter table county2
add column obamaCount integer;
commit;


/*having trouble with the aggregate by county issue*/

create table countystatus as
	select status.tweet_id, county4.geoid10
	from status inner join county4 on mbrcontains(county4.Geometry, status.coords);


insert into countycenter (romneyCount)
select count(romney.tweet_id)
	from romney inner join countycenter on contains(countycenter.Geometry, romney.coords)
	group by county2.GEOID10;


insert into county2 (obamaCount)
select count(obama.tweet_id) into county2.obamaCount
	from obama inner join county2 on contains(county2.Geometry, obama.coords)
	group by county2.GEOID10;

/*maybe these are the wrong approach*/
update status
	set countyfips = 
	(select countycenter.geoid10
	from status inner join countycenter 
	on closestpoint(countycenter.geometry, status.coords));

So new idea for processing - we can compare the the occurances of a word with the census variables
for a given county. i know that this is not good text parsing but it may be of interest

steps - 
1 find words of interest
2 loop through words of interest and find all tweets with those words
3 find the county that they are inside
4 find demographic variables of interest
5 see how they compare

we are clearly going to have to normalize around population
which will be pretty nice and easy to do
so it would be the number of times that a word is mentioned / people in area would be the twitter word rate
then we would look for covariance between the twitter word rate and other variables

the first thing to do would clearly be a comparison between tweets and population
we just need to get the total tweets for each county and see how it covaries with population
this should actually be a pretty cool map

