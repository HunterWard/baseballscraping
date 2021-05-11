import sqlalchemy
import pandas
from sqlalchemy.orm.session import *
import mydb

teams = []

def get_sfbb_df():
    url = 'https://www.smartfantasybaseball.com/PLAYERIDMAPCSV'

    data = pandas.read_csv(url, dtype={
        'MLBID': pandas.Int64Dtype(),
        })

    data['BIRTHDATE'] = pandas.to_datetime(data['BIRTHDATE'])

    return data

def clean_ssfb_df(df: pandas.DataFrame):
    """[summary] Cleaning for personal database purposes

    Args:
        df (pandas.DataFrame): [description]
    """

    newFrame = df
    newFrame.drop(['IDPLAYER',
            'PLAYERNAME',
            'LG',
            'FANGRAPHSNAME',
            'MLBNAME',
            'CBSNAME',
            'RETROID',
            'NFBCID',
            'NFBCNAME',
            'ESPNNAME',
            'KFFLNAME',
            'DAVENPORTID',
            'BPID',
            'YAHOONAME',
            'MSTRBLLNAME',
            'FANTPROSNAME',
            'ROTOWIREID',
            'FANDUELNAME',
            'FANDUELID',
            'DRAFTKINGSNAME',
            'OTTONEUID',
            'HQID',
            'RAZZBALLNAME',
            'FANTRAXID',
            'FANTRAXNAME',
            'ROTOWIRENAME',
            'NFBCLASTFIRST',
            'ALLPOS',
            ], inplace=True, axis=1)

    return newFrame[['MLBID', 'FIRSTNAME', 'LASTNAME', 'LASTCOMMAFIRST', 'BIRTHDATE', 'TEAM', 'POS', 'BATS', 'THROWS', 'CBSID', 'BREFID', 'IDFANGRAPHS', 'ESPNID', 'YAHOOID', 'ACTIVE']]



def to_sql_ignore(df: pandas.DataFrame, engine: sqlalchemy.engine, tablename: str):
    temp_table = tablename + '_temp'

    df.to_sql(con=conn, name=temp_table, index=False)

    with engine.begin() as cn:
        insert_sql = f'INSERT IGNORE INTO {tablename} (SELECT * FROM {temp_table})'
        cn.execute(insert_sql)
        drop_sql = f'DROP TABLE {temp_table}'
        cn.execute(drop_sql)



if __name__ == "__main__":

    a = get_sfbb_df()
    a = clean_ssfb_df(a)

    conn = mydb.getDBConPG()

    a.columns = map(str.lower, a.columns)

    a.to_sql(con=conn, name='player_info', index=False, if_exists='replace')
