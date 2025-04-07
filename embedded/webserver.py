import network
import socket

SSID = "PombaRiver"
PASSWORD = ""  # Open network

current_value = 0

def update_value(value):
    global current_value
    current_value = value
    print(f"Updated value: {current_value}")

def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=SSID, password=PASSWORD)
    while not ap.active():
        pass
    print("Access Point started with IP", ap.ifconfig()[0])

def start_web_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print("Web server running on:", addr)

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)

        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

<html>
    <head><title>Value Update</title></head>
    <body>
        <h1>Current Value: {current_value}</h1>
        <p>Update it by visiting: /update?value=NEW_NUMBER</p>
    </body>
</html>
"""
        conn.send(response)
        conn.close()
