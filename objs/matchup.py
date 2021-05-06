

from os import getpid


class Matchup():
    def __init__(self, hp, ap, ht, at, time, gid, tdate):
        self.gameid = gid

        self.gamedate = tdate

        self.homepitcher = hp
        self.awaypitcher = ap

        self.hometeam = ht
        self.awayteam = at

        self.currenttime = time

    def toString(self):
        print(self.currenttime)
        print(self.gameid)
        print(self.awayteam + ' @ ' + self.hometeam)
        print(self.awaypitcher['id'] + ': ' + self.awaypitcher['name'] + ' vs. ' + self.homepitcher['id'] + ': ' + self.homepitcher['name'])
