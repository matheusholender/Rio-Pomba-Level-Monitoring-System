import time
from machine import Pin, UART
import network
import socket
import _thread

text= "----------------------------------------------------------------\n" \
"Sistema de Medição Ultrassônico de Nivel do Rio Pomba\n" \
"Desenvolvido por Matheus V. Holender em parceria com a Eneltec\n" \
"----------------------------------------------------------------\n"

print(text)

# Define AP credentials
SSID = "PombaRiver"
PASSWORD = ""  # Open network (no password)

def start_ap():
    ap = network.WLAN(network.AP_IF)  # Access Point mode
    ap.active(True)  # Activate AP
    ap.config(essid=SSID, password=PASSWORD)  # Set SSID and password (empty for open network)

    while not ap.active():
        pass  # Wait until AP is active

    print("Access Point started with IP", ap.ifconfig()[0])

# Start the AP
start_ap()

# Global variable to store the number
current_value = 0

def update_value(new_value):
    """Updates the global value and serves it on the web server."""
    global current_value
    current_value = new_value
    print(f"Updated value: {current_value}")

last_measure=None

# MicroPython specific: Configure the UART
tx_pin=6
rx_pin=4

def calculate_parity_sum(data):
    return sum(data) & 0xFF  # Ensure only the low 8 bits are kept

def return_bytearray(distance_mm):
    if not (300 <= distance_mm <= 7500):
        raise ValueError("Distance out of range (300-7500mm)")
    
    high_byte = (distance_mm >> 8) & 0xFF
    low_byte = distance_mm & 0xFF
    
    command = [0xFB, 0x05, high_byte, low_byte]
    parity_sum = calculate_parity_sum(command)
    command.append(parity_sum)
    
    return command

def send_bytearray(code, ser):
    ser.read()  # Clear the buffer
    # Send the code here
    array = bytearray(return_bytearray(code))
    ser.write(array)

def read_bytearray(ser):
    # Read the response here
    response = ser.readline()
    return response

def set_threshold(threshold_mm):
    # Configure the UART
    print(threshold_mm)
    ser = UART(1, baudrate=9600, tx=tx_pin, rx=rx_pin)
    ser.init(bits=8, parity=None, stop=2)
    time.sleep(0.1)
    send_bytearray(threshold_mm, ser)
    time.sleep(0.5)
    if not read_bytearray(ser):
        time.sleep(0.3)
        set_threshold(threshold_mm)

def calculate_expected_response(distance_mm):
    # Ensure the distance is within the valid range
    if not (300 <= distance_mm <= 7500):
        raise ValueError("Distance out of range (300-7500mm)")
    
    # Convert the distance to high and low bytes
    high_byte = (distance_mm >> 8) & 0xFF
    low_byte = distance_mm & 0xFF
    
    # Create the expected response bytearray
    response_header = 0xFB  # Same as the sent command header
    response_command = 0x85  # Command ID for response
    checksum = calculate_parity_sum([response_header, response_command, high_byte, low_byte])
    
    # Build the response
    expected_response = bytearray([response_header, response_command, high_byte, low_byte, 0x00, checksum])
    
    return expected_response

def compare_responses(sent_distance, actual_response):
    # Calculate the expected response for the given distance
    expected_response = calculate_expected_response(sent_distance)
    print(f'Expected response: {expected_response}')
    print(f'Actual response: {actual_response}')
    # Compare expected and actual response
    if expected_response == actual_response:
        return True
    else:
        return False

def check_state():
    rx = Pin(rx_pin, Pin.OUT).value(0)
    state = Pin(rx_pin, Pin.IN).value()
    return state

def check_stability():
    data = []
    for i in range(100):
        data.append(check_state())
        time.sleep(0.05)
    if 0 in data and 1 in data:
        return False
    else:
        return True

def check_threshold(threshold_mm):
    set_threshold(threshold_mm-10)
    time.sleep(0.5)
    if not check_state():
        set_threshold(threshold_mm+10)
        time.sleep(0.5)
        if check_state():
            set_threshold(threshold_mm)
            return True
        else:
            set_threshold(threshold_mm)
            return False

def measure(min, max, step):
    for i in range(min, max, step):
        set_threshold(i)
        time.sleep(0.5)
        if check_state():
            return i


def run(last_measure, precision=500):
    print("Starting measurement sequence")
    first_measure = measure(300, 7500, precision)
    print(f"First measure: {first_measure - 500}~{first_measure}")
    precision = 100
    second_measure = measure(first_measure - 500, first_measure + 501, precision)
    print(f"Second measure: {second_measure - 100}~{second_measure}")
    precision = 10
    last_measure = measure(second_measure - 100, second_measure + 101, precision)
    if check_threshold(last_measure):
        print(f"Last measure: {last_measure}")
        return last_measure
    else:
        run(last_measure, 500)
    return last_measure

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
        
        # Send response with the current value
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

def measurement_thread():
    global current_value
    while True:
        new_measurement = float(run(last_measure)/10)
        update_value(new_measurement)
        time.sleep(5)  # Adjust the sleep time for how frequently measurements are updated

# Start the measurement thread
_thread.start_new_thread(measurement_thread, ())

# Run the web server in the main thread
start_web_server()

