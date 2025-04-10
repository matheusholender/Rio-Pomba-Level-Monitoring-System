from sensor import *
from webserver import *

HIGH_RANGE_ERROR = -3
LOW_RANGE_ERROR = -2
NO_SENSOR_ERROR = -1


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
    

def range_test():
    if set_threshold(7500):
        time.sleep(0.5)
        if not check_state_confirmed():
            print(f"{VERB.RED}{VERB.BOLD}Object out of detection range (+7500mm){VERB.ENDC}")
            return HIGH_RANGE_ERROR
    else: return NO_SENSOR_ERROR
    
    # Segundo, teste com 300 mm para verificar se o objeto está no range
    if set_threshold(300):
        time.sleep(0.5)
        if check_state_confirmed():
            print(f"{VERB.RED}{VERB.BOLD}Object out of detection range (-300mm){VERB.ENDC}")
            return LOW_RANGE_ERROR
    else: return NO_SENSOR_ERROR

import time
from machine import Pin, UART

# Variáveis globais para medição
start_time = None
response_time = None

def pin_callback(pin):
    global start_time, response_time
    # Confirma se a condição já não foi registrada
    if response_time is None and check_state():
        response_time = time.ticks_ms() - start_time

def estimate_response_time_irq():
    global start_time, response_time
    response_time = None

    # Garante que o sensor esteja em estado "False"
    print(f"{VERB.CYAN}Configurando threshold para 300 mm (estado inicial).{VERB.ENDC}")
    set_threshold(300)
    time.sleep(0.5)
    
    # Configura a interrupção para o pino de detecção
    sensor_pin = Pin(rx_pin, Pin.IN)
    sensor_pin.irq(trigger=Pin.IRQ_RISING, handler=pin_callback)
    
    print(f"{VERB.CYAN}Iniciando medição: configurando threshold para 7500 mm e iniciando timer...{VERB.ENDC}")
    start_time = time.ticks_ms()
    set_threshold(7500)
    
    # Aguarda até que a interrupção registre a resposta ou ocorra timeout
    timeout = 2000  # tempo máximo em ms para aguardar resposta
    while response_time is None and time.ticks_diff(time.ticks_ms(), start_time) < timeout:
        pass  # busy wait – nesse caso, o objetivo é capturar o tempo mais exato possível
    
    # Desativa a interrupção após a medição
    sensor_pin.irq(handler=None)
    
    if response_time is None:
        print(f"{VERB.RED}{VERB.BOLD}Timeout: Nenhuma resposta detectada em {timeout} ms.{VERB.ENDC}")
    else:
        print(f"{VERB.OKGREEN}Tempo de resposta medido: {response_time} ms{VERB.ENDC}")
    
    return response_time
