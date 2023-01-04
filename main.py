import machine
import network
from network import STA_IF
import secret

import socket
import time

led = machine.Pin("LED", machine.Pin.OUT)
led.off()


server = ('192.168.0.59', 38899)
#server = ('192.168.0.210', 2115)
turn_on = b'{"method":"setPilot","params":{"r":238,"b":2,"g":210,"dimming":10}}'
turn_off = b'{"method":"setPilot","params":{"state":false}}'


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secret.wifi['ssid'], secret.wifi['password'])
    while not wlan.isconnected():
        print('Waiting for connection...')
        time.sleep(1)
    led.on()
    return wlan.ifconfig()[0]


class Conn:
    def __init__(self, server):
        self.server = server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def send(self, data):
        self.sock.sendto(data, self.server)


c = Conn(server)
connect_wifi()
c.send(turn_on)
time.sleep(2)
c.send(turn_off)


