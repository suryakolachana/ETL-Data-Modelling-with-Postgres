A startup called Sparkify want to analyze the data they have been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to.
************************************************************************************************************************
Project Scope:

1) The main scope of the project is to build data modeling with Postgres and build an ETL pipeline using Python and the        Sparkify analytics team will work on the data results obtained.

2) As part of the project, As a Data Engineer I have to build data modeling with Postgres and build an ETL pipeline using      Python.On the database part, I have to create a postgres database called "SPARKIFY" and on the Database schema definition    side I have to define fact and dimension tables for a star schema for a particular analytic focus.On the ETL part, I have    to write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using        Python and SQL.
***************************************************************************************************************************
Project Design:
1) As a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis and to      build a database schema and ETL pipeline for this analysis.As part of the testing the postgres database and ETL pipeline,    queries will be provided by the analytics team from Sparkify and the expected results will be compared.
****************************************************************************************************************************
Project Data Sets:
1) As a Data Engineer Need to grab data user data from a directory of JSON logs on user activity on the app, as well as        songs data from a directory with JSON metadata on the songs in their app.
***************************************************************************************************************************
Song Data Set:
  1) Data/Song_Data
Log Data Set:
  2) Data/Log_Data

Project Steps:
************************************************************************
Postgres Database:
1) SPARKIFY

Star Schema for Song Play Analysis
*************************************************************************
Fact Table: 

1) songplays (records in log data associated with song plays)
*************************************************************************
Dimension Tables:

1) users  (users in the app)

2) songs  (songs in music database)

3) artists (artists in music database)

4) time: (timestamps of records in songplays broken down into specific units)
***************************************************************************************************************************
Python Scripts:
1) sql_queries.py performs following tasks mentioned below: 
   1) all the DROP statements to DROP tables if they exists 
   2) CREATE statements creates facts and dimension tables and specify all columns for each of the five tables with 
      right data types and conditions.
   3) INSERT statements will inserts records into each of the five tables below.
   4) A Query to get the song_id and artist id dynamically based on title, artist name, and duration of a song.
   5) create table queries and drop table queries which will be called in create_tables.py script.
2) create_tables.py performs following tasks mentioned below:
   1) The drop_tables function will drop each of the five tables if they exists.
   2) The create_tables Function creates facts and dimension tables and specify all columns for each of the five tables with       the right data types and conditions.
   3) The main Function creates the sparkify postgres database, drops tables if exists and create facts and dimension             tables.
3) etl.py performs the following tasks mentioned below:
   1) The song file and log file functions takes the cur object and filepath variables which process the song and log files,       and load into song, artists, time, user and songplays tables.
   2) The main Function takes the cur object,database connection to connect to sparkify database,filepath variables and           song/log files which extracts and processes all the log_data and song_data, and loads all the data into the five             tables.
************************************************************************************************************************   
Jupyter Notebook files:
   1) create_tables.ipynb will run create_tables.py to perform all the DDL and DML operations.
   2) test.ipnb will check the database conection and 'SELECT' statements are provided to query on the tables.
   3) etl.ipynb is given for verifying each command and data as well and then using those statements
      read and processes a single file from song_data and log_data and eventually loads into each of the five tables.
      copying everything into etl.py and running it into terminal using "python etl.py" and then running test.ipynb to see         whether data has been loaded in all the tables.
   4) Run.ipynb will run "Python etl.py"(etl process) which will read and processes all the files from song_data and l             log_data directories and eventually loads processed Data into each of the five fact and dimesion tables.
***************************************************************************************************************************
Execution Order:
    1) %run -i create_tables.py
    2) test.ipnb (to check all the tables got created and data got loaded)
    2) %run -i etl.py
    3) test.ipnb (To check the counts and all the data got loaded into each of the five tables).
    
    (Note: Run order-Wise)
****************************************************************************************************************************
Queries to check:

 1) select count(*) from songplays;----6820 records
 2) select count(*) from users;----96 records
 3) select count(*) from songs;----71 records
 4) select count(*) from artists;---69 records
 5) select count(*) from time;------6813 records
 6) SELECT distinct * FROM songplays a,songs b,artists c where a.song_id = b.song_id \
    and b.artist_id = c.artist_id \
    and a.artist_id = b.artist_id;------1 record got matched
    
**************************************************************************************************************************** 
Data Cleaning: 
   1)  Using json and pandas libraries creating a panda df read to read the data from the external Directories.
   
        df = pd.read_json('data/song_data/A/B/C/TRABCAJ12903CDFCC2.json',lines=True)
        
   2) Extracting Data from data sets and doing the etl process to load into the Individual fact and Dimension tables.
    
        song_data     =   df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0]
        artist_data   = df[['artist_id','artist_name','artist_location','artist_latitude', 'artist_longitude']].values[0]
        time_data     = ([t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday])
        user_data     = df.loc[:,['userId','firstName','lastName','gender','level']]
        songplay_data = (row.ts_datetime,row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        
   3) Identified and removed duplicates.
   4) Got rid of extra spaces.
   5) Extracted the timestamp, hour, day, week of year, month, year, and weekday from the ts column into a time table.
   6) Selecting only specific columns to read from the dataset.
     ****************************************************************************************************************************
Handled Data Integrity Issues:

 1) Data Integrity is the maintainance of, and the assuarance of the accuracy and consistency of the data.
 2) It is a critical aspect to design and implement a system which stores,processes or retrieves data.

An example of how data integrity constraint is taken care of while loading into a Users table.
    (Duplicated Data before the load) 
 1)  	userId	firstName	lastName	gender	level
	       8	Kaylee	    Summers	    F	    free
	       8	Kaylee	    Summers	    F	    free
	       8	Kaylee	    Summers	    F	    free
	       8	Kaylee	    Summers	    F	    free
	       8	Kaylee	    Summers	    F	    free

   (Processed Data after the load)      
     SELECT * FROM users where user_id = 8;

     user_id	first_name	last_name	gender	level
      8 	    Kaylee	    Summers	    F	free
***************************************************************************************************************************
