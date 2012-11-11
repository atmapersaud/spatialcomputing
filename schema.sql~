
begin;
/*turn on the foreign keys*/
/*this seems to not run but everything seems to work fine*/


create table twitteruser (
	created_at text, /*remember to use time here*/
	description text,
	followers_count integer,/* count of followers for a user */
	friends_count integer, /* count of people person is following */
	geo_enabled text(1), /*boolean if it is geo-enabled*/
	user_id text(20) primary key,
	lang text(4), /*not sure on length on this i think it is two*/
	location text,/* make sure to trigger this to location, and grab more data */
	name text(20), /*make sure to check length */
	screen_name text,
	status text, /*current status*/
	statuses_count integer,
	time_zone text,
	url text,
	utc_offset integer, /*offset in seconds from utc*/
	verified text(1)
);

create table status (
	created_at text(20), /* make sure to use datetime here */
	current_user_retweet text(1), /*marks if the user themselves have retweeted this tweet*/
	favorited text(1),/*marks if the user themselves have favorited this tweet*/
	tweet_id text(20) not null primary key,
	in_reply_to_status text(20),/*make these reference other tweets*/
	in_reply_to_user_id text(20),/*make this reference users table*/
	place text(100),/*link this to the place table with triggers */
	retweet_count int,
	retweeted text(1),
	source text(40), /* this tells you if it is from the web, phone, iPhone and what not, pretty nice */
	tweet_text text(160),
	user_id int(20),
	foreign key (user_id) references twitteruser(user_id)
);

SELECT AddGeometryColumn('status', 'coords', 4326, 'POINT', 'XY');
SELECT CreateSpatialIndex('status', 'coords');

/* twitter has its own geography, which we should also use */
/*use their api t ograb these */
create table place (
	attributes text,
	bounding_box blob, /* trigger it to a table */
	country text,
	country_code text(2), /*link this to a table with all iso-2 codes */
	full_name text,
	place_id text(20) primary key,
	name text,
	place_type text, /*maybe subtype this out to possible options */
	url text /* good to keep, could actually go out and grab geojson from the url */
);

/*this is a table for the followers of a user*/
/*this table is not getting populated because we are not getting any data for it*/
create table follow (
	userId text,
	follow text,
	primary key (userId, follow),
	foreign key (userId) references twitteruser(userid),
	foreign key (follow) references twitteruser(userid)
);

/*this could be worth looking into*/
create table mention (
	tweet_id text(20),
	user_id text(20),
	start_index integer,
	finish_index integer,
	primary key (tweet_id, user_id, start_index),
	foreign key (tweet_id) references tweet(tweet_id),
	foreign key (user_id) references tweeteruser(user_id)	
);

/*for some reason the url is not coming through*/
create table tweeturl (
	tweet_id text(20),
	url_short text,
	url_expanded text,
	start_index integer,
	end_index integer,
	primary key (tweet_id, url_expanded, start_index),
	foreign key (tweet_id) references status(tweet_id)
);

/*this might be nice to have an index on hashs*/
/*should we make a similar way to interact with each word, url, etc?*/
create table hash_tweet (
	tweet_id text(20),
	hash text,
	start_index integer(3),
	end_index integer(3),
	primary key (hash, tweet_id, start_index),
	foreign key (tweet_id) references status(tweet_id)
);

create table words (
	word text,
	tweet_id integer,
	word_number integer,
	primary key (tweet_id, word_number),
	foreign key (tweet_id) references status(tweet_id)
);

/*SELECT AddGeometryColumn('words', 'coords', 4326, 'POINT', 'XY');
SELECT CreateSpatialIndex('words', 'coords');*/

commit;
