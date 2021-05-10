import datetime
import json
from bs4 import BeautifulSoup
import requests
#from xbaseballAPI.baseballscraping.objs.matchup import *
#from objs.matchup import Matchup
import time as timy
from xbaseballAPI.baseballscraping.objs.matchup import Matchup

def getProbables():
    todaysdate = datetime.date.today()

    url = f'https://www.mlb.com/probable-pitchers/{todaysdate}'
    headrs = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    page = requests.get(url)
    soup = BeautifulSoup(page.text,  'html5lib')

    elements = soup.select('div[class*="probable-pitchers__matchup"]')

    matchups = []
    muDict = {}

    # Element is the container on MLB.com which holds all the information of an upcoming game
    for element in elements:
        # Basic info parsing
        names = element.find_all('div', class_='probable-pitchers__pitcher-name')
        away = element.find('span', class_='probable-pitchers__team-name probable-pitchers__team-name--away').get_text().strip()
        home = element.find('span', class_='probable-pitchers__team-name probable-pitchers__team-name--home').get_text().strip()

        # Gametime parsing
        # TODO: Parse out each of these individually and set time to equal the state.  Not needed as of 5/5/21, setting all to 'TBD'
        # It will correctly parse out what inning a game is currently in
        if (element.find('span', class_='probable-pitchers__game-state probable-pitchers__game-state--tbd') != None or
            element.find('span', class_='probable-pitchers__game-state probable-pitchers__game-state--postponed') != None or
            element.find('span', class_='probable-pitchers__game-state probable-pitchers__game-state--delayed') != None or
            element.find('span', class_='probable-pitchers__game-state probable-pitchers__game-state--warmup') != None):
                time = 'TBD'
        elif (element.find('span', class_='probable-pitchers__game-state probable-pitchers__game-state--final') != None):
            time = 'Final'
        else:
            time = element.find('time').get_text().strip()


        if (time[:5] == 'Delay'):
            timeSTR = 'Delay | ' + time.split(' ')[-2] + ' ' + time.split(' ')[-1]
            time = timeSTR

        if '\u2022' in time:
            time = time.replace('\u2022', '|')

        # Deal with TBA pitchers
        awaypitcher = {
            'id': 'N/A',
            'name': names[0].get_text().strip(),
        }

        if names[0].find('a') != None:
            awaypitcher['id'] = names[0].find('a').get('href').split('-')[-1]

        homepitcher = {
            'id': 'N/A',
            'name': names[1].get_text().strip(),
        }

        if names[1].find('a') != None:
            homepitcher['id'] = names[1].find('a').get('href').split('-')[-1]

        # Game ID comes from button at the bottom of the element
        if (element.find('div', class_='p-button p-button--regular probable-pitchers__button') == None):
            continue

        buttonText = element.find('div', class_='p-button p-button--regular probable-pitchers__button').find('a').get('href')

        gameid = None
        if (buttonText.split('/')[-1] == 'preview'):
            gameid = buttonText.split('/')[-2]
        else:
            gameid = buttonText.split('/')[-1]

        # Finished games prepend a 'g' to the id for some reason
        if gameid[0] == 'g':
            gameid = gameid[1:]

        mu = Matchup(homepitcher, awaypitcher, home, away, time, gameid, todaysdate.__str__())

        matchups.append(mu.__dict__)

    muDict['data'] = matchups
    return muDict


if __name__ == '__main__':
    print(getProbables())