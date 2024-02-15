import socket
import tkinter as tk
from PIL import ImageTk , Image
import io
import time

format="utf-8"
def on_click(event):
    x, y = event.x, event.y
    x=str(x)
    y=str(y)
    client_socket2.send(x.encode(format))
    client_socket2.send(y.encode(format))
    print((x,y))
    

host='127.0.0.1'
port1=12345
port2=5535
size=1024
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port1))

image_data = b""
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    image_data += data

# Save the received image data to a file
with open('map2.jpg', 'wb') as file:
    file.write(image_data)

client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket2.connect((host,port2))
print("If no message is coming , you must wait. Max Players reached!!")
choice=input((client_socket2.recv(size).decode(format)))
client_socket2.send(choice.encode(format))
choice=int(choice)
root = tk.Tk()
root.title("Click the Location Game")

image = Image.open("map2.jpg")
photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
label = tk.Label(root, image=photo)
label.image = photo
label.pack()

if (choice==1):
    flag=0
    print(client_socket2.recv(size).decode(format))
    msg=input()
    client_socket2.send(msg.encode(format))
    print(client_socket2.recv(size).decode(format))
    print(client_socket2.recv(size).decode(format))
    money=input()
    client_socket2.send(money.encode(format))
    label.bind("<Button-1>",on_click)
    root.mainloop()
    time.sleep(30)
    exit


if (choice==2):
    print(client_socket2.recv(size).decode(format))
    msg=input()
    client_socket2.send(msg.encode(format))
    print(client_socket2.recv(size).decode(format))
    print(client_socket2.recv(size).decode(format))
    money=input()
    client_socket2.send(money.encode(format))
    label.bind("<Button-1>",on_click)
    print("You must close map window after clicking!")
    root.mainloop()
    print(client_socket2.recv(size).decode(format))
    time.sleep(30)
    