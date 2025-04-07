import time
from machine import Pin, UART

tx_pin = 6
rx_pin = 4

def calculate_parity_sum(data):
    return sum(data) & 0xFF

def return_bytearray(distance_mm):
    if not (300 <= distance_mm <= 7500):
        raise ValueError("Distance out of range (300-7500mm)")
    high_byte = (distance_mm >> 8) & 0xFF
    low_byte = distance_mm & 0xFF
    command = [0xFB, 0x05, high_byte, low_byte]
    command.append(calculate_parity_sum(command))
    return command

def send_bytearray(code, ser):
    ser.read()
    ser.write(bytearray(return_bytearray(code)))

def read_bytearray(ser):
    return ser.readline()

def set_threshold(threshold_mm):
    ser = UART(1, baudrate=9600, tx=tx_pin, rx=rx_pin)
    ser.init(bits=8, parity=None, stop=2)
    time.sleep(0.1)
    send_bytearray(threshold_mm, ser)
    time.sleep(0.5)
    if not read_bytearray(ser):
        time.sleep(0.3)
        set_threshold(threshold_mm)

def check_state():
    Pin(rx_pin, Pin.OUT).value(0)
    return Pin(rx_pin, Pin.IN).value()

def check_threshold(threshold_mm):
    set_threshold(threshold_mm - 10)
    time.sleep(0.5)
    if not check_state():
        set_threshold(threshold_mm + 10)
        time.sleep(0.5)
        if check_state():
            set_threshold(threshold_mm)
            return True
        else:
            set_threshold(threshold_mm)
            return False

def measure(min_val, max_val, step):
    for i in range(min_val, max_val, step):
        set_threshold(i)
        time.sleep(0.5)
        if check_state():
            return i
    return max_val  # fallback in case no threshold triggers

def run(precision=500):
    print("Starting fresh measurement sequence...")

    first = measure(300, 7500, precision)
    print(f"First: {max(300, first - 500)} ~ {first}")

    second_min = max(300, first - 500)
    second_max = min(7500, first + 500)
    second = measure(second_min, second_max + 1, 100)
    print(f"Second: {max(300, second - 100)} ~ {second}")

    last_min = max(300, second - 100)
    last_max = min(7500, second + 100)
    last = measure(last_min, last_max + 1, 10)
    print(f"Last: {last}")

    if check_threshold(last):
        print(f"Final measurement: {last}")
        return last
    else:
        print("Measurement unstable. Restarting...")
        return run(500)
