class Room:
    def __init__(self,host,players,id,chosen_location):
        self.id=id
        self.host=host
        self.players=players
        self.start=0
        self.chosen_location=chosen_location
        self.win_id=-1
class Player:
    def __init__(self,id,location,points,conn):
        self.id=id
        self.location=location
        self.points=points
        self.conn=conn
        self.dis=0


players=[]
players.append(Player(0,1,2,3))
players.append(Player(4,1,2,3))
players.append(Player(5,1,2,3))

players[1].id=2
print(players[1].id)