import machine
import network
from network import STA_IF
import secret
from microdot import Microdot
import socket
import time

led = machine.Pin("LED", machine.Pin.OUT)
led.off()

server = ('192.168.0.59', 38899)
# server = ('192.168.0.210', 2115)
turn_on = b'{"method":"setPilot","params":{"r":238,"b":2,"g":210,"dimming":10}}'
turn_off = b'{"method":"setPilot","params":{"state":false}}'


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secret.wifi['ssid'], secret.wifi['password'])
    while not wlan.isconnected():
        print('Waiting for connection...')
        time.sleep(1)
    return wlan.ifconfig()[0]


class Conn:
    def __init__(self, server):
        self.server = server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        self.sock.sendto(data, self.server)


connect_wifi()
led.on()

app = Microdot()
c = Conn(server)

@app.route('/')
def index(request):
    print(request.body)
    c.send(request.body)
    return 'Hello, world!'


app.run(port=80)
