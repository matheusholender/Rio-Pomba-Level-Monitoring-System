import _thread
import time
import sensor
import webserver
from boot import VERB



print(VERB.CYAN +"------------------------------------------------------------------")
print(VERB.HEADER +"     Sistema de Medição Ultrassônico de Nivel do Rio Pomba")
print(VERB.YELLOW +"  Desenvolvido por Matheus V. Holender em parceria com a Eneltec")
print(VERB.YELLOW +"                           04/2025")
print(VERB.CYAN +"------------------------------------------------------------------\n"+VERB.ENDC)


def measurement_thread():
    while True:
        value,precision = sensor.run_binary() 
        #webserver.update_value(value)
        if value is not None:
            print(f"{VERB.OKGREEN}Distance: {float(value/ 10)} (±{precision/10} cm)\n{VERB.ENDC}")
        time.sleep(5)
        

#webserver.start_ap()
measurement_thread()
#webserver.start_web_server()
