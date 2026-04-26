import socket
import time
import math
import random
import json

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

c = 0

while True:
    #accelerometer values
    x = math.sin(c)
    y = math.sin(0.3 * c)
    z = math.sin(1.9 * c)

    #1-pressed, 0-released
    button = random.randint(0, 1)

    message = {
        "accelerometer" :[x, y, z], 
        "button_1" : button
    }

    print(message)

    #convert to string
    message = json.dumps(message)

    sock.sendto(message.encode(), (IP, PORT))

    c += 1
    time.sleep(1)
