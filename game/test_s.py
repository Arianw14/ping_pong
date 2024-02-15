import threading
import socket
import time
import math
flag=0
id1=0
id2=0
ip=''
flag_sum=0
port=12345
size=1024
format="utf-8"
players=[]
rooms=[]
room_ids=[]
clients=[]
c_count=0
max_p=4

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((ip,5535))
server_socket.listen()

class Room:
    def __init__(self,host,players,id,chosen_location):
        self.id=id
        self.host=host
        self.players=players
        self.start=0
        self.chosen_location=chosen_location
        self.win_id=-1
        self.count=0
        self.click_count=0
class Player:
    def __init__(self,id,location,points,conn):
        self.id=id
        self.location=location
        self.points=points
        self.conn=conn
        self.dis=0

def game_check(room_index):
    l1=rooms[room_index].chosen_location
    for p in rooms[room_index].players:
        p.dis=math.sqrt((l1[0]-p.location[0])**2+(l1[1]-p.location[1])**2)
        print(p.dis)
    min_index=0
    i=0
    min_pd=rooms[room_index].players[0].dis
    for p in rooms[room_index].players:
        if min_pd>p.dis:
            min_index=i
        i=i+1
    p=rooms[room_index].players[min_index]
    return(p)

def search_add(room_ids,id):
    
    if(id in room_ids):
        return(room_ids.index(id))
    else:
        return(-1)
    
def send_all(p1,room_index):
    msg=f"The winner of  is the player with id:{p1.id}"
    print(msg)
    for  p in rooms[room_index].players:
        p.conn.send(msg.encode(format))
    
    
def final_g(client_socket,room_index,player_index,role):
    global c_count
    client_socket.send("Starting the game...".encode(format))
    client_socket.send("Pay 1 Rs for 1 sec of game:".encode(format))
    time1=int(client_socket.recv(size).decode(format))
    s1=time.time()
    print(time1)
    z=0
    if(role==1):
            if(z==0):
                client_socket.send("Click on the location after all players join\n Dont click on anything after this for 30 seconds!".encode(format))
            else:
                client_socket.send("Click on new location!".encode(format))
            x=int(client_socket.recv(size).decode(format))
            y=int(client_socket.recv(size).decode(format))
            l=(x,y)
            players[player_index].location=l
            rooms[room_index].chosen_location=l
            print(rooms[room_index].chosen_location)
            while(rooms[room_index].click_count<rooms[room_index].count):
                time.sleep(1)
            p = game_check(room_index)
            print(p.id)
            s2=time.time()
            bura=s2-s1
            if(bura>time1):
                client_socket.send("Timeout!".encode(format))
                print(f"Timeout!!!! for player with id:{player_index}")
                exit()
            send_all(p,room_index)
            c_count=c_count-1
            client_socket.close()
    if(role==0):
            rooms[room_index].count=rooms[room_index].count+1
            client_socket.send("Click on the location".encode(format))
            x=int(client_socket.recv(size).decode(format))
            y=int(client_socket.recv(size).decode(format))
            l=(x,y)
            print(l)
            players[player_index].location=l
            print(l)
            rooms[room_index].click_count=rooms[room_index].click_count+1
            time.sleep(30)
            rooms[room_index].click_count=0
            s2=time.time()
            bura=s2-s1
            if(bura>time1):
                client_socket.send("Timeout!".encode(format))
                print(f"Timeout!!!! for player with id:{player_index}")
                exit()
            c_count=c_count-1
            client_socket.close()

def game():
    global flag
    global id1
    global id2
    global c_count
    flag=1
    while True:
        global server_socket
        client_socket,addr=server_socket.accept()
        print(f"Game Client connected with address:{addr}")
        p=Player(id1,(0,0),0,client_socket)
        players.append(p)
        id1=id1+1
        c_count=c_count+1
        print(c_count)
        while(c_count>max_p):
            time.sleep(1)
        client_socket.send("Press 1 to create room, Press 2 to join room:".encode(format))
        choice=int(client_socket.recv(size).decode(format))
        if choice==1:
            rooms.append(Room(client_socket,[],id2,(0,0)))
            room_ids.append(id2)
            id2=id2+1
            print(rooms)
            print(room_ids)
            client_socket.send("You are the host.\nYou will click on the location and write its name.\n Others will guess it\nSend any digit to start game:".encode(format))
            if(client_socket.recv(size).decode(format)):
                rooms[id2-1].start=1
               # print(rooms[id2-1].id)
                final_g(client_socket,id2-1,id1-1,1)
        if(choice==2):
            if(room_ids==[]):
                client_socket.send(f"You have to become the host , for no rooms are created for now \n Send any digit to start".encode(format))
                if(client_socket.recv(size).decode(format)):
                    rooms.append(Room(client_socket,[],id2,(0,0)))
                    room_ids.append(id2)
                    id2=id2+1
                    rooms[id2-1].start=1
                    client_socket.send("You are the host.\nYou will click on the location and write its name.\n Others will guess it".encode(format))
               #    print(rooms[id2-1].id)
                    final_g(client_socket,id2-1,id1-1,1)
            else:
                msg=f"Your id is {id1-1}. \n Enter an id out of the following ids :{room_ids}"
                client_socket.send(msg.encode(format))
                id_room=int(client_socket.recv(size).decode(format))
                k=search_add(room_ids,id_room)
                #print(f"k={k}")
                if(k==-1):
                    client_socket.send("You didn't enter valid room id".encode(format))
                else:
                    client_socket.send("Joined room successfully!".encode(format))
                    rooms[k].players.append(p)
                    final_g(client_socket,k,id1-1,0)

def handle_client(client_socket,addr):
        
        with open('1.jpg', 'rb') as file:
            image_data = file.read()

    # Send the image data to the client
        client_socket.sendall(image_data)
        client_socket.close()
        game()
def main():
    server_socket1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket1.bind((ip,port))
    server_socket1.listen()   
    while True:
        client_socket,addr=server_socket1.accept()
        print(f"Client connected with address:{addr}")
        clients.append((client_socket,addr))
        client_handler=threading.Thread(target=handle_client,args=(client_socket,addr))
        client_handler.start()
        print(f"The number of clients is {threading.active_count()-1}")

if __name__=="__main__":
    main()