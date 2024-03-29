import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This Function takes the cur method and filepath variable which process the song file, and load data into song and           artists tables.
     
    Paramaters:     
       cur: Cursor Method to Execute.
       filepath: Song data filepath.
    
    Returns:
       None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude', 'artist_longitude']].values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This Function takes the cur method and filepath variable which process the log file, and load data into time, user and       songplays tables.
    
    Paramaters:     
       cur: Cursor Method to Execute.
       filepath: Log data filepath.
    
    Returns:
       None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.query("page=='NextSong'");

    # convert timestamp column to datetime
    t = t = df["ts"]
    t = pd.to_datetime(t, unit = 'ms')
    
    # insert time data records
    time_data     = ([t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday])
    column_labels = (['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday'])
    zip_data      = zip(column_labels,time_data)
    dict_data     = dict(zip_data)
    time_df       = pd.DataFrame(dict_data).reset_index(drop=True)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.loc[:,['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records    
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data =        (pd.to_datetime(row.ts,unit='ms'),row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This Function takes the cur method to execute,database connection to connect to sparkify database,filepath variables and     song/log process file function which extracts and processes the log_data and song_data, and loads data into the five         tables.
    
    Paramaters:     
       cur: Cursor Method to Execute.
       conn: Database Connection.
       filepath: Song/Log data filepaths.
       func: process_song_file/process_log_file function.
    
    Returns:
       None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    This Main Function Executes the Process_data function with the respective parameters provided.
    
    Paramaters:     
     None
    
    Returns:
     None
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()