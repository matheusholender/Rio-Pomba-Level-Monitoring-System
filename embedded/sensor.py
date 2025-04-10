import time
from machine import Pin, UART

# Classe para estilizar os prints no terminal
class VERB:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN = '\033[96m'

# Pinos do sensor (ajuste conforme necessário)
tx_pin = 6
rx_pin = 4

# Utilitários para comunicação serial
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

# Define o threshold de detecção
def set_threshold(threshold_mm):
    ser = UART(1, baudrate=9600, tx=tx_pin, rx=rx_pin)
    ser.init(bits=8, parity=None, stop=2)
    time.sleep(0.1)
    send_bytearray(threshold_mm, ser)
    time.sleep(0.5)
    # Se não houver resposta, tenta novamente
    if not read_bytearray(ser):
        time.sleep(0.3)
        set_threshold(threshold_mm)

# Lê o estado de detecção (True se detectado, False caso contrário)
def check_state():
    # Configura o pino rx temporariamente como saída para ajudar na leitura
    Pin(rx_pin, Pin.OUT).value(0)
    return Pin(rx_pin, Pin.IN).value()

# Confirmação de leitura: realiza várias leituras e decide com base na maioria
def check_state_confirmed(repetitions=100, delay=0.001):
    true_count = 0
    false_count = 0
    for _ in range(repetitions):
        if check_state():
            true_count += 1
        else:
            false_count += 1
        time.sleep(delay)
    return true_count > false_count

# Verifica a estabilidade do threshold final
def check_threshold(threshold_mm):
    set_threshold(threshold_mm)
    time.sleep(0.5)
    return check_state_confirmed()

# Busca binária com verificação por maioria
def measure_binary(min_val=300, max_val=7500, tolerance=10):
    low = min_val
    high = max_val

    while (high - low) > tolerance:
        mid = (low + high) // 2
        print(f"{VERB.YELLOW}Threshold: {mid} mm{VERB.ENDC}")
        set_threshold(mid)
        time.sleep(0.5)
        if check_state_confirmed():
            high = mid
        else:
            low = mid + 1

    final = (low + high) // 2
    return final

# Função principal para rodar a medição com busca binária
def run_binary(tolerance=10):
    # Primeiro, teste com 7500 mm para verificar se o objeto está no range
    set_threshold(7500)
    time.sleep(0.5)
    if not check_state_confirmed():
        print(f"{VERB.RED}{VERB.BOLD}Object out of detection range (+7500mm){VERB.ENDC}")
        return None
    
    # Segundo, teste com 300 mm para verificar se o objeto está no range
    set_threshold(300)
    time.sleep(0.5)
    if check_state_confirmed():
        print(f"{VERB.RED}{VERB.BOLD}Object out of detection range (-300mm){VERB.ENDC}")
        return None
    print(f"{VERB.OKGREEN}{VERB.BOLD}Starting measurement...{VERB.ENDC}")
    start = time.ticks_ms()
    result = measure_binary(300, 7500, tolerance)

    elapsed = time.ticks_diff(time.ticks_ms(), start)
    print(f"{VERB.OKBLUE}Elapsed time: {elapsed} ms{VERB.ENDC}")
    return result, tolerance
