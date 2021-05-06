import utils, mydb
import pandas
import numpy as np
import datetime, sys
import hashlib
from pandas.core.arrays.integer import Int16Dtype, Int32Dtype
import sqlalchemy
#from xbaseballAPI.baseballscraping.mydb import getDBCon


def general_data_from_search(team, year, playertype="pitcher", date1="", date2="", addid=False):
    """Gets data from Baseball Savant's search function.  This function gets every pitch event in the given time frame. The playertype
    argument decides whether you get batter or pitcher data.

    If creating an exhaustive database, note that you can get overlapping data because one teams pitcher data will return the same events
    of another teams batter data with the only change being the "player_name" field.  See 'addid' if interested in adding a unique event id
    for simple duplicate detection.

    Args:
        team (string): Team abbreviation in form 'XXX'
        year (int): Year number between 2012-2021 in form YYYY
        playertype (str, optional): Either 'pitcher' or 'batter'. Defaults to "pitcher".
        date1 (str, optional): The bottom date range to search for. Defaults to empty string. yyyy-mm-dd
        date2 (str, optional): The top date range to search for. Defaults to empty string. yyyy-mm-dd
        addid (bool, optional): Adds a custom ID.  Defaults False.
        clean (bool, optional): Clean data for DB. Defaults True.

    Returns:
        pandas dataframe: dateframe of every event from search parameters
    """

    url = ("https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB="
            f"&hfGT=R%7CPO%7C&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea={year}%7C&hfSit="
            f"&player_type={playertype}&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt={date1}"
            f"&game_date_lt={date2}&hfInfield=&team={team}&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfBBT="
            "&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=api_p_release_speed"
            "&sort_order=desc&min_pas=0&type=details&")

    # Read in the csv and specify certain columns to have nullable int types
    scrapedData = pandas.read_csv(url, dtype={
        'zone': pandas.Int16Dtype(),
        'hit_location': pandas.Int16Dtype(),
        'on_1b': pandas.Int32Dtype(),
        'on_2b': pandas.Int32Dtype(),
        'on_3b': pandas.Int32Dtype(),
        'hit_distance_sc': pandas.Int16Dtype(),
        'launch_angle': pandas.Int16Dtype(),
        'release_spin_rate': pandas.Int32Dtype(),
        'launch_speed_angle': pandas.Int16Dtype(),
        'spin_axis': pandas.Int32Dtype()
    })

    # Data comes with columns that will always be empty **EVEN IN YEARS WHERE THIS DATA WAS NOT DEPRECATED, ITS ALL DELETED**
    # Dropping player name, pitcher.1 and fielder_2.1 because they are duplicates of other rows
    scrapedData.drop(['umpire',
                      'spin_dir',
                      'spin_rate_deprecated',
                      'break_angle_deprecated',
                      'break_length_deprecated',
                      'tfs_deprecated',
                      'tfs_zulu_deprecated',
                      'player_name',
                      'pitcher.1',
                      'fielder_2.1'], axis=1, inplace=True)

    scrapedData.rename(columns={"type":"type_"}, inplace=True)

    if (addid): addPitchIds(scrapedData)

    return scrapedData

def addPitchIds(dataframe):
    """Uses SHA256 along with information from dataframe row to generate a unique ID for the pitch.  sv_id value supplied in original data
    isn't unique and isn't supplied for all events.

    DF information used in hash:
        game_pk       - Game ID number
        game_date     - Game date in type of string, format YYYY-MM-DD
        batter        - BS batter ID
        pitcher       - BS pitcher ID
        at_bat_number - Game at bat number
        pitch_number  - Pitch number of game

    The above data is available throughout all of pitchfx/statcast history.  In testing, there were no recorded collisions with this data.

    Args:
        dataframe (pandas dataframe): Dataframe from get_data_from_search fn
    """

    dataframe['pitchid'] = dataframe.apply(lambda row: hashlib.sha256((row['game_pk']).to_bytes(256, 'big') +
                                                               (row['game_date']).encode('utf-8') +
                                                               (row['batter']).to_bytes(256, 'big') +
                                                               (row['pitcher']).to_bytes(256, 'big') +
                                                               (row['at_bat_number']).to_bytes(256, 'big') +
                                                               (row['pitch_number']).to_bytes(256, 'big')
                                                               ).digest().upper(), axis = 1)

    return dataframe


if __name__ == "__main__":
    df = general_data_from_search('LAD', 2021, addid=True)
    #$print(df.head())
    #print(df.head(7))
    #df.to_csv('final.csv', index=False)

    conn = mydb.getDBCon()



    mydb.addDFtoDatabase(df, conn,'pitch_event')
