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
def set_threshold(threshold_mm, retries=50):
    ser = UART(1, baudrate=9600, tx=tx_pin, rx=rx_pin)
    ser.init(bits=8, parity=None, stop=2)
    time.sleep(0.1)

    for attempt in range(retries):
        send_bytearray(threshold_mm, ser)
        time.sleep(0.5)

        if read_bytearray(ser):
            return True  # sucesso

        time.sleep(0.3)

    print(f"{VERB.RED}Error: Sensor not found.{VERB.ENDC}")
    return False  # falha após todas as tentativas

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

def estimate_response_time():
    """
    Estima o tempo de resposta do sensor.
    Primeiro, garante que o sensor esteja em estado False definindo o threshold para 300 mm.
    Em seguida, define o threshold para 7500 mm e inicia a contagem do tempo
    até que check_state() retorne True.
    """
    # Garante que o sensor comece com estado False
    print(f"{VERB.CYAN}Configurando threshold para 300 mm (estado inicial).{VERB.ENDC}")
    set_threshold(300)
    time.sleep(0.5)  # Pequena pausa para estabilizar o estado
    if check_state():
        print(f"{VERB.YELLOW}Atenção: check_state retornou True em 300 mm. Verifique a conexão ou o sensor!{VERB.ENDC}")
    
    # Inicia o tempo a partir do set para 7500 mm
    print(f"{VERB.CYAN}Configurando threshold para 7500 mm e iniciando medição do tempo de resposta...{VERB.ENDC}")
    start = time.ticks_ms()
    set_threshold(7500)
    
    # Espera ativamente até que check_state() retorne True (detecta o objeto)
    while not check_state():
        pass  # Aguarda sem adicionar delays extras para medir o tempo puro
    
    response_time = time.ticks_diff(time.ticks_ms(), start)
    print(f"{VERB.OKGREEN}Tempo de resposta estimado: {response_time} ms{VERB.ENDC}")
    return response_time


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
    print(f"{VERB.OKGREEN}{VERB.BOLD}Starting measurement...{VERB.ENDC}")
    start = time.ticks_ms()
    result = measure_binary(300, 7500, tolerance)

    elapsed = time.ticks_diff(time.ticks_ms(), start)
    print(f"{VERB.OKBLUE}Elapsed time: {elapsed} ms{VERB.ENDC}")
    return result, tolerance
