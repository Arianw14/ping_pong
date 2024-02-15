import socket
import threading
import time

id1=0
id2=0
ip=''
port=12345
size=1024
format="utf-8"
players=[]
rooms=[]
room_ids=[]
clients=[]

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
        

def search_add(room_ids,id):
    
    if(id in room_ids):
        return(room_ids.index(id))
    else:
        return(-1)

def game_check(room_index):
    l1=rooms[room_index].chosen_location
    for p in rooms[room_index].players:
        p.dis=(l1[0]-p.location[0])**2+(l1[1]-p.location[1])**2
    min_index=0
    i=0
    min_pd=rooms[room_index].players[0]
    for p in rooms[room_index].players:
        if min_pd<p.dis:
            min_index=i
        i=i+1
    return(p)

def send_all(p1,room_index):
    msg=f"The winner of this round is the player with id:{p1.id}"
    for p in rooms[room_index].players:
        p.conn.send(msg).encode(format)
    



def final_g(client_socket,room_index,player_index,role): 
    client_socket.send("Starting the game...".encode(format))
    if(role==1):
        while True:
            client_socket.send("Click on the location".encode(format))
            l=client_socket.recv(size).decode(format)
            rooms[room_index].chosen_location=l
            time.sleep(30)
            p = game_check(room_index)
            send_all(p,room_index)
    if(role==0):
         while True:
            client_socket.send("Click on the location".encode(format))
            l=client_socket.recv(size).decode(format)
            players[player_index].location=l
            time.sleep(30)


def game():
    port=5335
    ip=''
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((ip,port))
    server_socket.listen()
    client_socket,addr=server_socket.accept()
    p=Player(id1,(0,0),0,client_socket)
    players.append(p)
    id1=id1+1
    client_socket.send("Press 1 to create room, Press 2 to join room:".encode(format))
    choice=int(client_socket.recv(size).decode(format))
    if(choice==1):
        rooms.append(Room(client_socket,p,[],id2,(0,0)))
        room_ids.append(id2)
        id2=id2+1
        client_socket.send("You are the host.\nYou will click on the location and write its name.\n Others will guess it\nPress any key to start game:".encode(format))
        if(client_socket.recv(size).decode(format)):
            rooms[id2-1].start=1
            final_g(client_socket,id2-1,id1-1,1)

    if(choice==2):
        msg=f"Enter an id out of the following ids :{room_ids}"
        client_socket.send(msg.encode(format))
        id_room=int(client_socket.recv(size).decode(format))
        k=search_add(room_ids,id_room)
        if(k==-1):
            client_socket.send("You didn't enter valid room id".encode(format))
        else:
            rooms[k].players.append(p)
            while(rooms[k].start==0):
                time.sleep(1)
            if(rooms[k].start==1):
                final_g(client_socket,k,id1-1,0)


def main():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((ip,port))
    server_socket.listen()   

    def handle_client(client_socket,addr):
        with open('1.jpg', 'rb') as file:
            image_data = file.read()

    # Send the image data to the client
        client_socket.sendall(image_data)
        client_socket.close()
        game()




    while True:
        client_socket,addr=server_socket.accept()
        print(f"Client connected with address:{addr}")
        clients.append((client_socket,addr))
        client_handler=threading.Thread(target=handle_client,args=(client_socket,addr))
        client_handler.start()
        print(f"The number of clients is {threading.active_count()-1}")

if __name__=="__main__":
    main()