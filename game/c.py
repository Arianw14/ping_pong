import socket
import tkinter as tk
from PIL import ImageTk , Image
import io
import time


def on_click(event):
    x, y = event.x, event.y
    location = f"{x},{y}"
    print(location)
   # client_socket.send(location.encode())

host='127.0.0.1'
port=12345
size=1024
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

image_data = b""
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    image_data += data

# Save the received image data to a file
with open('map2.jpg', 'wb') as file:
    file.write(image_data)
root = tk.Tk()
root.title("Click the Location Game")

image = Image.open("map2.jpg")
photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
label = tk.Label(root, image=photo)
label.image = photo
label.pack()

label.bind("<Button-1>",on_click)

root.mainloop()

 







