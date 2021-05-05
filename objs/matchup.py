

class Matchup():
    def __init__(self, hp, ap, ht, at, time):
        self.homepitcher = hp
        self.awaypitcher = ap

        self.hometeam = ht
        self.awayteam = at

        self.gametime = time

    def toString(self):
        print(self.gametime)
        print(self.awayteam + ' @ ' + self.hometeam)
        print(self.awaypitcher['id'] + ': ' + self.awaypitcher['name'] + ' vs. ' + self.homepitcher['id'] + ': ' + self.homepitcher['name'])


if __name__ == "__main__":
    x = Matchup(669203, 608223, 14, 15, '7:55')

    print(x.toString())