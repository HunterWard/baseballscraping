

class Matchup():
    def __init__(self, p1, p2, t1, t2, time):
        self.pitcher1 = p1
        self.team1 = t1
        self.team1TBA = False

        self.pitcher2 = p2
        self.team2 = t2
        self.team2TBA = False

        self.gametime = time

    def toString(self):
        return f"Game Time: {self.gametime}\nTeam1: {self.team1}, Pitcher: {self.pitcher1} | Team2: {self.team2}, Pitcher: {self.pitcher2}"

if __name__ == "__main__":
    x = Matchup(669203, 608223, 14, 15, '7:55')

    print(x.toString())