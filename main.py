import machine
import network
import envs
from microdot import Microdot
import socket
import time

led = machine.Pin("LED", machine.Pin.OUT)
led.off()

server = (envs.device_address, envs.device_port)


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(envs.wifi_ssid, envs.wifi_password)
    while not wlan.isconnected():
        print('Waiting for connection...')
        time.sleep(1)
    return wlan.ifconfig()[0]


class Conn:
    def __init__(self, _server):
        self.server = _server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        self.sock.sendto(data, self.server)


def blink():
    led.on()
    led.off()


connect_wifi()

app = Microdot()
c = Conn(server)


def authenticate_user(request):
    value = request.headers.get("Authorization")
    if not value:
        return None
    if not value.lower().startswith('basic'):
        return None
    auth = value[6:]
    if not auth == envs.auth:
        return None
    return True


@app.before_request
def authorize(request):
    led.on()
    authorized = authenticate_user(request)
    if not authorized:
        return 'Unauthorized', 401
    request.g.authorized = authorized


@app.after_request
def after(req, res):
    led.off()


@app.route('/')
def index(request):
    print(request.body)
    c.send(request.body)
    return '¡Éxito! :)'


app.run(port=80)
