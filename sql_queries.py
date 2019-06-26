# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"


# CREATE TABLES

songplay_table_create = ("CREATE TABLE IF NOT EXISTS songplays(songplay_id SERIAL, start_time timestamp NOT NULL, user_id int NOT NULL, level varchar, song_id varchar, artist_id varchar, session_id varchar, location varchar, user_agent varchar,CONSTRAINT pk_on_songplay_id PRIMARY KEY(songplay_id))")

user_table_create = ("CREATE TABLE IF NOT EXISTS users(user_id int NOT NULL,first_name varchar,last_name varchar,gender varchar,level varchar,CONSTRAINT pk_on_user_id PRIMARY KEY(user_id))")

song_table_create = ("CREATE TABLE IF NOT EXISTS songs(song_id varchar NOT NULL, title varchar, artist_id varchar, year int, duration float,CONSTRAINT pk_on_song_id PRIMARY KEY(song_id))")

artist_table_create = ("CREATE TABLE IF NOT EXISTS artists(artist_id varchar NOT NULL, artist_name varchar, artist_location varchar, artist_latitude float, artist_longitude float,CONSTRAINT pk_on_artist_id PRIMARY KEY(artist_id))")

time_table_create = ("CREATE TABLE IF NOT EXISTS time(start_time timestamp NOT NULL, hour int, day int, week int, month int, year int, weekday int,CONSTRAINT pk_on_start_time PRIMARY KEY(start_time))")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays(start_time,user_id,level,song_id,artist_id,session_id, location,user_agent)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)ON CONFLICT(songplay_id) DO UPDATE SET level = EXCLUDED.level""")

user_table_insert = ("""INSERT INTO users(user_id,first_name,last_name,gender,level)VALUES(%s,%s,%s,%s,%s)ON CONFLICT
(user_id) DO UPDATE SET level = EXCLUDED.level""")

song_table_insert = ("""INSERT INTO songs(song_id,title,artist_id,year,duration)VALUES(%s,%s,%s,%s,%s)ON
CONFLICT(song_id) DO NOTHING""")

artist_table_insert = ("""INSERT INTO artists(artist_id,artist_name,artist_location,artist_latitude,artist_longitude)
values(%s,%s,%s,%s,%s)ON CONFLICT(artist_id) DO NOTHING""")


time_table_insert = ("""INSERT INTO time(start_time,hour,day,week,month,year,weekday)VALUES(%s,%s,%s,%s,%s,%s,%s)ON CONFLICT(start_time) DO NOTHING""")



# FIND SONGS

song_select = ("""select a.song_id,b.artist_id from songs a,artists b where a.artist_id = b.artist_id and a.title = (%s) and b.artist_name = (%s) and a.duration = (%s)""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]