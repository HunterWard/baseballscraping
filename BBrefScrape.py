import pandas as pd
import json
import datetime

"""
dfs = pd.read_html('https://baseballsavant.mlb.com/savant-player/brandon-woodruff-605540?stats=statcast-r-pitching-mlb', attrs={'id':'detailedPitches'})
for df in dfs:
    x = df.to_json(orient='records')
    print(x)
"""

def getCurrentDivisionStandings(league, division):
    if (league == 'AL'):
        if (division == 'C'):
            dfs = pd.read_html('https://www.baseball-reference.com/leagues/AL/2021-standings.shtml', attrs={'id':'standings_C'})
            return dfs[0].to_json(orient='records', indent=2)
        elif (division == 'W'):
            dfs = pd.read_html('https://www.baseball-reference.com/leagues/AL/2021-standings.shtml', attrs={'id':'standings_W'})
            return dfs[0].to_json(orient='records', indent=2)
        elif (division == 'E'):
            dfs = pd.read_html('https://www.baseball-reference.com/leagues/AL/2021-standings.shtml', attrs={'id':'standings_E'})
            return dfs[0].to_json(orient='records', indent=2)
    elif (league == 'NL'):
        if (division == 'C'):
            dfs = pd.read_html('https://www.baseball-reference.com/leagues/NL/2021-standings.shtml', attrs={'id':'standings_C'})
            return dfs[0].to_json(orient='records', indent=2)
        elif (division == 'W'):
            dfs = pd.read_html('https://www.baseball-reference.com/leagues/NL/2021-standings.shtml', attrs={'id':'standings_W'})
            return dfs[0].to_json(orient='records', indent=2)
        elif (division == 'E'):
            dfs = pd.read_html('https://www.baseball-reference.com/leagues/NL/2021-standings.shtml', attrs={'id':'standings_E'})
            return dfs[0].to_json(orient='records', indent=2)
    return None
